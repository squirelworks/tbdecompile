#include "handler.hpp"

#include <cctype>

namespace {

bool is_text(unsigned char c) {
    return c == 9 || c == 10 || c == 13 || (c >= 32 && c < 127);
}

std::string lower(std::string s) {
    for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    return s;
}

bool starts_with_ci(const unsigned char* p, size_t n, const char* lit) {
    size_t i = 0;
    for (; lit[i]; ++i) {
        if (i >= n) return false;
        if (std::tolower(p[i]) != std::tolower(static_cast<unsigned char>(lit[i]))) return false;
    }
    return true;
}

std::string hex_of(const unsigned char* p, size_t n) {
    static const char* k = "0123456789abcdef";
    std::string s;
    s.resize(n * 2);
    for (size_t i = 0; i < n; ++i) {
        s[i * 2] = k[p[i] >> 4];
        s[i * 2 + 1] = k[p[i] & 0xf];
    }
    return s;
}

void take_quotes(const std::string& text, std::vector<std::string>& out) {
    for (size_t i = 0; i < text.size(); ++i) {
        if (text[i] != '"') continue;
        size_t j = text.find('"', i + 1);
        if (j == std::string::npos || j - i > 40) continue;
        out.push_back(text.substr(i + 1, j - i - 1));
        i = j;
    }
}

void take_comments(const std::string& text, std::vector<std::string>& out) {
    for (size_t i = 0; i < text.size(); ++i) {
        if (text[i] != '{') continue;
        size_t j = text.find('}', i + 1);
        if (j == std::string::npos || j - i > 80) continue;
        out.push_back(text.substr(i + 1, j - i - 1));
        i = j;
    }
}

}  // namespace

Handler split_handler(const unsigned char* data, size_t n, size_t file_offset) {
    Handler h;
    h.offset = file_offset;
    size_t i = 0;
    while (i < n && is_text(data[i])) ++i;
    std::string head(reinterpret_cast<const char*>(data), i);
    auto sp = head.find_last_of(" \t");
    h.kind = sp == std::string::npos ? head : head.substr(sp + 1);
    while (!h.kind.empty() && (h.kind.back() == '.' || h.kind.back() == '-')) h.kind.pop_back();

    size_t at = 0;
    while (at < n) {
        if (is_text(data[at])) {
            size_t b = at;
            while (at < n && is_text(data[at])) ++at;
            if (at - b >= 2) {
                std::string text(reinterpret_cast<const char*>(data + b), at - b);
                h.source_runs.push_back(SourceRun{file_offset + b, text});
                if (!h.source.empty()) h.source.push_back(' ');
                h.source += text;
                take_quotes(text, h.quotes);
                take_comments(text, h.comments);
            }
        } else {
            size_t b = at;
            while (at < n && !is_text(data[at])) ++at;
            OpcodeRun run;
            run.offset = file_offset + b;
            run.bytes.assign(data + b, data + at);
            h.opcode_runs.push_back(std::move(run));
        }
    }

    std::string low = lower(h.source);
    h.mentions_tries = low.find("tries") != std::string::npos;
    h.mentions_incorrect = low.find("incorrect") != std::string::npos;
    // The closing brace of a comment is often an opcode, so scan the joined
    // source for "--{" and keep the text that follows.
    for (size_t i = 0; i + 3 < h.source.size(); ++i) {
        if (h.source.compare(i, 3, "--{") != 0) continue;
        size_t j = h.source.find('}', i + 3);
        size_t stop = j == std::string::npos ? std::min(h.source.size(), i + 48) : j;
        std::string c = h.source.substr(i + 3, stop - (i + 3));
        if (!c.empty()) h.comments.push_back(c);
        if (j == std::string::npos) break;
        i = j;
    }
    bool retry = low.find("try again") != std::string::npos || low.find("try aagain") != std::string::npos;
    bool go = low.find("go") != std::string::npos;
    for (const auto& q : h.quotes) {
        if (q.empty() || (q[0] != 'P' && q[0] != 'p')) continue;
        if (retry) h.retry_pages.push_back(q);
        if (go) h.go_pages.push_back(q);
    }
    // Tokenized Go from the corpus: e0, then "--{Go ", then 80 91 <arg> b1 ...
    // The argument is not a page name. Keep the operand bytes and do not invent one.
    for (const auto& run : h.opcode_runs) {
        const auto& b = run.bytes;
        for (size_t k = 0; k + 3 < b.size(); ++k) {
            if (b[k] == 0x80 && b[k + 1] == 0x91) {
                size_t m = k + 2;
                std::string op;
                while (m < b.size() && b[m] != 0xb1 && op.size() < 8) {
                    op.push_back(static_cast<char>(b[m]));
                    ++m;
                }
                h.unresolved_ops.push_back(hex_of(reinterpret_cast<const unsigned char*>(op.data()), op.size()));
            }
        }
    }
    return h;
}

std::vector<Handler> split_handlers(const unsigned char* page, size_t n, size_t file_offset) {
    std::vector<Handler> out;
    for (size_t i = 0; i + 10 < n; ++i) {
        if (!starts_with_ci(page + i, n - i, "to handle ")) continue;
        size_t end = i + 10;
        size_t limit = std::min(n, i + 4000);
        while (end + 3 <= limit) {
            if (end > i + 10 && starts_with_ci(page + end, n - end, "to handle ")) break;
            if ((page[end] == 'E' || page[end] == 'e') &&
                (page[end + 1] == 'N' || page[end + 1] == 'n') &&
                (page[end + 2] == 'D' || page[end + 2] == 'd') &&
                (end + 3 == n || !std::isalnum(page[end + 3]))) {
                end += 3;
                break;
            }
            ++end;
        }
        if (end == i + 10) end = std::min(n, i + 240);
        out.push_back(split_handler(page + i, end - i, file_offset + i));
        i = end - 1;
    }
    return out;
}
