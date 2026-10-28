// Run one initializeTest and one buttonClick against a live page.
//   g++ -std=c++17 -O2 -o tbk_script openscript.cpp handler.cpp path.cpp session.cpp script.cpp
//   ./tbk_script lesson.tbk lessons/9e954d01.json P1290

#include "openscript.hpp"

#include <cstring>
#include <fstream>
#include <iostream>
#include <iterator>
#include <vector>

namespace {

const unsigned char kMark[] = {0x80, 0x65, 0x00, 0x05, 0x00, 0x02, 0x02};

std::vector<unsigned char> read_file(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("cannot open " + path);
    return std::vector<unsigned char>(std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>());
}

std::string cstr_at(const std::vector<unsigned char>& b, size_t off, size_t n) {
    std::string s;
    for (size_t i = 0; i < n && off + i < b.size(); ++i) {
        unsigned char c = b[off + i];
        if (c == 0 || c < 32 || c > 126) break;
        s.push_back(static_cast<char>(c));
    }
    return s;
}

}  // namespace

int cmd_script(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "usage: tbk_script <lesson.tbk> <lesson.json> <page>\n";
        return 2;
    }
    Lesson lesson = load_lesson(argv[2]);
    BookState book = open_lesson(lesson);
    book = go(std::move(book), argv[3]);
    auto init = run_send(book, "initializeTest");
    std::cout << "live " << page_of(book).id << " score " << book.session.score
              << " after " << init.target << "\n";

    auto data = read_file(argv[1]);
    std::vector<size_t> hits;
    for (size_t i = 0; i + sizeof(kMark) <= data.size(); ++i)
        if (std::memcmp(data.data() + i, kMark, sizeof(kMark)) == 0) hits.push_back(i);
    const unsigned char* blob = nullptr;
    size_t n = 0;
    size_t off = 0;
    for (size_t k = 0; k < hits.size(); ++k) {
        if (cstr_at(data, hits[k] + 11, 32) != argv[3]) continue;
        off = hits[k];
        size_t nxt = k + 1 < hits.size() ? hits[k + 1] : data.size();
        blob = data.data() + off;
        n = nxt - off;
        break;
    }
    if (!blob) {
        std::cerr << "no page " << argv[3] << "\n";
        return 1;
    }
    auto handlers = split_handlers(blob, n, off);
    std::cout << "handlers " << handlers.size() << "\n";
    for (const auto& handler : handlers) {
        bool correct = !handler.mentions_incorrect;
        auto ran = run_handler(book, handler, correct);
        std::cout << ran.handler << " " << ran.action << " " << ran.target
                  << " opcodes " << ran.opcodes.size() << " now " << page_of(book).id << "\n";
        if (ran.action == "go") break;
    }
    return 0;
}
