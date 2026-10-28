// Walk a Maybe2 lesson shell the way systemshell/shell.ts does.
//   g++ -std=c++17 -O2 -o tbk_path path.cpp session.cpp walk.cpp
//   ./tbk_path lessons/9e954d01.json /tmp/recs

#include "path.hpp"

#include <iostream>

int cmd_path(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: tbk_path <lesson.json> [record-dir]\n";
        return 2;
    }
    Lesson lesson = load_lesson(argv[1]);
    BookState book = open_lesson(lesson);
    std::cout << lesson.id << "  " << lesson.title
              << "  pages " << lesson.pages.size()
              << "  shells";
    for (const auto& s : lesson.shells) std::cout << " " << s;
    std::cout << "\nmenu";
    for (const auto& item : lesson.menu) std::cout << " [" << item.label << " -> " << item.page << "]";
    std::cout << "\n";

    book = go(std::move(book), "P100");
    book = follow_label(book, "Next");
    std::cout << "after Next from P100: " << page_of(book).id << "\n";

    book = go(std::move(book), "P1290");
    const ShellPage& q = page_of(book);
    std::cout << q.id << "  " << (q.text.empty() ? "" : q.text[0]) << "\n";
    std::cout << "again " << q.quiz.again << " next " << q.quiz.next << "\n";
    int correct_at = -1;
    for (size_t i = 0; i < q.quiz.choices.size(); ++i) {
        std::cout << "  " << (q.quiz.choices[i].correct ? "*" : " ") << " " << q.quiz.choices[i].label << "\n";
        if (q.quiz.choices[i].correct) correct_at = static_cast<int>(i);
    }
    book = answer_quiz(std::move(book), true);
    std::cout << "answer correct -> " << page_of(book).id
              << "  score " << book.session.score << "\n";

    int quizzes = 0;
    int right = 0;
    for (const auto& page : lesson.pages) {
        if (!page.quiz.present) continue;
        ++quizzes;
        for (const auto& c : page.quiz.choices) if (c.correct) ++right;
    }
    std::cout << "quiz pages " << quizzes << " with a marked correct choice " << right << "\n";

    if (argc >= 3 && correct_at >= 0) {
        SessionFile sessions(argv[2]);
        int id = sessions.start(lesson.id, "student");
        sessions.write_response(id, graded_response(q, static_cast<uint16_t>(correct_at + 1), true, 1));
        auto rec = sessions.read(id);
        std::cout << "SESSION3 index " << id
                  << " response " << sessions.response_path(rec.file_index).filename().string()
                  << " flag " << static_cast<int>(sessions.read_responses(rec.file_index)[0].flag)
                  << "\n";
    }
    return 0;
}
