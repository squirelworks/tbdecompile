#pragma once

#include "session.hpp"

#include <string>
#include <vector>

// Path and quiz from Maybe2, not from the unpacked NE host.
//
// maybe2/translate.py already built the page graph for a processed book:
// Next/Back items, quoted jumps, and quiz choices with a correct flag.
// maybe2/systemshell/shell.ts walks that graph. gotoPageList goes to the
// first jump. answerQuiz records correct/wrong and follows quiz.next.
// This is that shell. It does not decode OpenScript opcodes.

struct Choice {
    std::string label;
    bool correct = false;
};

struct Item {
    std::string label;
    std::string page;
};

struct Quiz {
    bool present = false;
    std::vector<Choice> choices;
    std::string again;
    std::string next;
};

struct ShellPage {
    std::string id;
    std::string kind;
    std::vector<std::string> text;
    std::vector<std::string> jumps;
    std::vector<std::string> sends;
    std::vector<Item> items;
    Quiz quiz;
};

struct Lesson {
    std::string id;
    std::string title;
    std::vector<std::string> shells;
    std::vector<ShellPage> pages;
    std::vector<Item> menu;
};

struct SessionState {
    bool open = false;
    std::vector<std::pair<std::string, bool>> responses;
    std::string bookmark;
    int score = 0;
};

struct BookState {
    const Lesson* lesson = nullptr;
    size_t index = 0;
    std::vector<std::string> log;
    SessionState session;
    int help_from = -1;
};

Lesson load_lesson(const std::string& path);
BookState open_lesson(const Lesson& lesson);
const ShellPage& page_of(const BookState& book);
BookState go(BookState book, const std::string& id);
BookState send(BookState book, const std::string& name, const std::string& arg = {});
BookState answer_quiz(BookState book, bool correct);
BookState follow_label(BookState book, const std::string& label);

// Pack a Maybe2 grade into the 0x1e response record. flag 1 is the stand-in
// for correct, flag 2 for wrong. The DLL itself does not score.
ResponseRecord graded_response(const ShellPage& page, uint16_t choice, bool correct, uint16_t n);
