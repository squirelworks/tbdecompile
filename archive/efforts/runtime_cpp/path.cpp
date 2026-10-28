#include "path.hpp"

#include <algorithm>
#include <cctype>
#include <cstring>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>

namespace {

std::string read_all(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("cannot open " + path);
    return std::string(std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>());
}

struct Parser {
    std::string s;
    size_t i = 0;
    explicit Parser(std::string in) : s(std::move(in)) {}
    void skip() {
        while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) ++i;
    }
    bool eat(char c) {
        skip();
        if (i < s.size() && s[i] == c) { ++i; return true; }
        return false;
    }
    std::string str() {
        skip();
        if (i >= s.size() || s[i] != '"') return {};
        ++i;
        std::string out;
        while (i < s.size() && s[i] != '"') {
            if (s[i] == '\\' && i + 1 < s.size()) {
                ++i;
                if (s[i] == 'n') out.push_back('\n');
                else out.push_back(s[i]);
            } else out.push_back(s[i]);
            ++i;
        }
        if (i < s.size()) ++i;
        return out;
    }
    void skip_value() {
        skip();
        if (i >= s.size()) return;
        if (s[i] == '"') { str(); return; }
        if (s[i] == '{') {
            eat('{');
            while (!eat('}') && i < s.size()) { str(); eat(':'); skip_value(); eat(','); }
            return;
        }
        if (s[i] == '[') {
            eat('[');
            while (!eat(']') && i < s.size()) { skip_value(); eat(','); }
            return;
        }
        while (i < s.size() && s[i] != ',' && s[i] != '}' && s[i] != ']') ++i;
    }
};

std::vector<std::string> string_list(Parser& p) {
    std::vector<std::string> out;
    p.eat('[');
    while (!p.eat(']') && p.i < p.s.size()) {
        out.push_back(p.str());
        p.eat(',');
    }
    return out;
}

void note(BookState& book, const std::string& line) {
    book.log.push_back(line);
    if (book.log.size() > 12) book.log.erase(book.log.begin());
}

BookState at(BookState book, const std::string& id) {
    for (size_t i = 0; i < book.lesson->pages.size(); ++i) {
        if (book.lesson->pages[i].id == id) {
            book.index = i;
            note(book, "go " + id);
            return book;
        }
    }
    note(book, "no page " + id);
    return book;
}

}  // namespace

Lesson load_lesson(const std::string& path) {
    Parser p(read_all(path));
    Lesson lesson;
    p.eat('{');
    while (!p.eat('}') && p.i < p.s.size()) {
        std::string key = p.str();
        p.eat(':');
        if (key == "id") lesson.id = p.str();
        else if (key == "title") lesson.title = p.str();
        else if (key == "shells") lesson.shells = string_list(p);
        else if (key == "menu") {
            p.eat('[');
            while (!p.eat(']') && p.i < p.s.size()) {
                Item item;
                p.eat('{');
                while (!p.eat('}') && p.i < p.s.size()) {
                    std::string k = p.str();
                    p.eat(':');
                    if (k == "label") item.label = p.str();
                    else if (k == "page") item.page = p.str();
                    else p.skip_value();
                    p.eat(',');
                }
                lesson.menu.push_back(item);
                p.eat(',');
            }
        } else if (key == "pages") {
            p.eat('[');
            while (!p.eat(']') && p.i < p.s.size()) {
                ShellPage page;
                p.eat('{');
                while (!p.eat('}') && p.i < p.s.size()) {
                    std::string k = p.str();
                    p.eat(':');
                    if (k == "id") page.id = p.str();
                    else if (k == "kind") page.kind = p.str();
                    else if (k == "text") page.text = string_list(p);
                    else if (k == "jumps") page.jumps = string_list(p);
                    else if (k == "sends") page.sends = string_list(p);
                    else if (k == "items") {
                        p.eat('[');
                        while (!p.eat(']') && p.i < p.s.size()) {
                            Item item;
                            p.eat('{');
                            while (!p.eat('}') && p.i < p.s.size()) {
                                std::string ik = p.str();
                                p.eat(':');
                                if (ik == "label") item.label = p.str();
                                else if (ik == "page") item.page = p.str();
                                else p.skip_value();
                                p.eat(',');
                            }
                            page.items.push_back(item);
                            p.eat(',');
                        }
                    } else if (k == "quiz") {
                        page.quiz.present = true;
                        p.eat('{');
                        while (!p.eat('}') && p.i < p.s.size()) {
                            std::string qk = p.str();
                            p.eat(':');
                            if (qk == "again") page.quiz.again = p.str();
                            else if (qk == "next") page.quiz.next = p.str();
                            else if (qk == "choices") {
                                p.eat('[');
                                while (!p.eat(']') && p.i < p.s.size()) {
                                    Choice c;
                                    p.eat('{');
                                    while (!p.eat('}') && p.i < p.s.size()) {
                                        std::string ck = p.str();
                                        p.eat(':');
                                        if (ck == "label") c.label = p.str();
                                        else if (ck == "correct") {
                                            p.skip();
                                            c.correct = p.s.compare(p.i, 4, "true") == 0;
                                            p.skip_value();
                                        } else p.skip_value();
                                        p.eat(',');
                                    }
                                    page.quiz.choices.push_back(c);
                                    p.eat(',');
                                }
                            } else p.skip_value();
                            p.eat(',');
                        }
                    } else p.skip_value();
                    p.eat(',');
                }
                lesson.pages.push_back(page);
                p.eat(',');
            }
        } else p.skip_value();
        p.eat(',');
    }
    return lesson;
}

const ShellPage& page_of(const BookState& book) { return book.lesson->pages[book.index]; }

BookState go(BookState book, const std::string& id) {
    book.help_from = -1;
    return at(std::move(book), id);
}

BookState answer_quiz(BookState book, bool correct) {
    const ShellPage& page = page_of(book);
    auto& rows = book.session.responses;
    rows.erase(std::remove_if(rows.begin(), rows.end(),
                              [&](const auto& row) { return row.first == page.id; }),
               rows.end());
    rows.emplace_back(page.id, correct);
    int right = 0;
    for (const auto& row : rows) if (row.second) ++right;
    book.session.score = rows.empty() ? 0 : (100 * right) / static_cast<int>(rows.size());
    if (!page.quiz.next.empty()) return at(std::move(book), page.quiz.next);
    note(book, "answer");
    return book;
}

BookState follow_label(BookState book, const std::string& label) {
    const ShellPage& page = page_of(book);
    if (page.id == "P900") {
        note(book, "menu has no next");
        if (label == "Next" || label == "Back") return book;
    }
    if (page.id == "P300" && label.find("IBM") != std::string::npos) {
        note(book, "selection1 nida81.tbk P310");
        return book;
    }
    for (const auto& item : page.items) {
        if (item.label != label || item.page.empty()) continue;
        // A nida81 P20001 switch is the shell menu. Inside this lesson it
        // returns to the in-book lesson menu, which is P900.
        if (item.page == "P20001" && (label == "Back" || label == "Menu" || label == "Exit")) {
            if (label == "Exit") {
                note(book, "lesson exit");
                return book;
            }
            return go(std::move(book), "P900");
        }
        return go(std::move(book), item.page);
    }
    note(book, "no item " + label);
    return book;
}

BookState send(BookState book, const std::string& name, const std::string& arg) {
    if (name == "initializeBase" || name == "initializeTrnr") {
        note(book, name);
        return book;
    }
    if (name == "initializeRecs") {
        book.session = {};
        note(book, name);
        return book;
    }
    if (name == "initializeTest") {
        book.session.score = 0;
        note(book, name);
        return book;
    }
    if (name == "openSession") {
        book.session.open = true;
        note(book, name);
        return book;
    }
    if (name == "bookmarkSession") {
        book.session.bookmark = arg.empty() ? page_of(book).id : arg;
        note(book, "bookmarkSession " + book.session.bookmark);
        return book;
    }
    if (name == "gotoPageList" || name == "setupQuizPage") {
        std::string id = arg.empty() && !page_of(book).jumps.empty() ? page_of(book).jumps[0] : arg;
        note(book, name + (id.empty() ? "" : " " + id));
        return id.empty() ? book : at(std::move(book), id);
    }
    if (name == "enterSystem") {
        note(book, name);
        for (const char* call : {"initializeBase", "initializeRecs", "initializeTest", "initializeTrnr", "openSession"})
            book = send(std::move(book), call);
        return book;
    }
    note(book, "send " + name + " (no module)");
    return book;
}

BookState open_lesson(const Lesson& lesson) {
    BookState book;
    book.lesson = &lesson;
    book = send(std::move(book), "enterSystem");
    for (const auto& name : page_of(book).sends) book = send(std::move(book), name);
    return book;
}

ResponseRecord graded_response(const ShellPage& page, uint16_t choice, bool correct, uint16_t n) {
    ResponseRecord r;
    r.word0 = n;
    r.word1 = choice;
    r.word2 = static_cast<uint16_t>(page.quiz.choices.size());
    r.flag = correct ? 1 : 2;
    std::memset(r.label, 0, sizeof(r.label));
    std::memcpy(r.label, page.id.data(), std::min(sizeof(r.label) - 1, page.id.size()));
    return r;
}
