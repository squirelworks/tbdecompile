// Paint one page the way Maybe3 reader.js does.
//   g++ -std=c++17 -O2 -o tbk_paint graphics.cpp paint.cpp
//   ./tbk_paint lesson.tbk P400 out.svg

#include "graphics.hpp"

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

int cmd_paint(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: tbk_paint <lesson.tbk> <page> [out.svg]\n";
        return 2;
    }
    auto data = read_file(argv[1]);
    std::string want = argv[2];
    std::vector<size_t> hits;
    for (size_t i = 0; i + sizeof(kMark) <= data.size(); ++i) {
        if (std::memcmp(data.data() + i, kMark, sizeof(kMark)) == 0) hits.push_back(i);
    }
    for (size_t n = 0; n < hits.size(); ++n) {
        if (cstr_at(data, hits[n] + 11, 32) != want) continue;
        size_t nxt = n + 1 < hits.size() ? hits[n + 1] : data.size();
        PageGraphic page = read_page_graphic(data.data() + hits[n], nxt - hits[n], want, hits[n]);
        std::cout << page.name << " fields " << page.fields.size()
                  << " draw-sites " << page.sites.size()
                  << " picture " << (page.picture.in_page ? "in page" : "not in page") << "\n";
        std::cout << page.picture.note << "\n";
        for (const auto& f : page.fields) {
            std::cout << "  " << f.x << "," << f.y << " " << f.w << "x" << f.h
                      << (f.chip ? " chip" : "") << "  " << f.text.substr(0, 60) << "\n";
        }
        if (argc >= 4) {
            std::ofstream out(argv[3]);
            out << paint_svg(page);
            std::cout << "wrote " << argv[3] << "\n";
        }
        return 0;
    }
    std::cerr << "no page " << want << "\n";
    return 1;
}
