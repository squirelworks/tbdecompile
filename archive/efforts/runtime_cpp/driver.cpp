// Driver for the handler splitter and the SESSION3 stand-in.
//   g++ -std=c++17 -O2 -o tbk_standin handler.cpp session.cpp standin.cpp driver.cpp
//   ./tbk_standin lesson.tbk P1080 /tmp/recs

#include "handler.hpp"
#include "session.hpp"
#include "standin.hpp"

#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

const unsigned char kMark[] = {0x80, 0x65, 0x00, 0x05, 0x00, 0x02, 0x02};

std::vector<unsigned char> read_file(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("cannot open " + path);
    in.seekg(0, std::ios::end);
    std::vector<unsigned char> b(static_cast<size_t>(in.tellg()));
    in.seekg(0);
    if (!b.empty()) in.read(reinterpret_cast<char*>(b.data()), static_cast<std::streamsize>(b.size()));
    return b;
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

int cmd_standin(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: tbk_standin <lesson.tbk> <page> [record-dir]\n";
        return 2;
    }
    auto data = read_file(argv[1]);
    std::string want = argv[2];
    std::vector<size_t> hits;
    for (size_t i = 0; i + sizeof(kMark) <= data.size(); ++i) {
        if (std::memcmp(data.data() + i, kMark, sizeof(kMark)) == 0) hits.push_back(i);
    }
    const unsigned char* blob = nullptr;
    size_t n = 0;
    size_t off = 0;
    for (size_t k = 0; k < hits.size(); ++k) {
        if (cstr_at(data, hits[k] + 11, 32) != want) continue;
        off = hits[k];
        size_t nxt = k + 1 < hits.size() ? hits[k + 1] : data.size();
        blob = data.data() + off;
        n = nxt - off;
        break;
    }
    if (!blob) {
        std::cerr << "no page " << want << "\n";
        return 1;
    }
    auto handlers = split_handlers(blob, n, off);
    StandIn info = stand_in_for(handlers);
    std::cout << want << " handlers " << handlers.size()
              << " question " << (info.is_question ? "yes" : "no") << "\n";
    std::cout << "note  " << info.note << "\n";
    for (const auto& h : handlers) {
        std::cout << "-- " << h.kind << " source-runs " << h.source_runs.size()
                  << " opcode-runs " << h.opcode_runs.size() << "\n";
        std::cout << "   source " << h.source.substr(0, 180) << "\n";
        std::cout << "   quotes " << h.quotes.size() << " comments " << h.comments.size() << "\n";
        if (!h.retry_pages.empty()) {
            std::cout << "   retry";
            for (const auto& p : h.retry_pages) std::cout << " " << p;
            std::cout << "\n";
        }
        if (!h.unresolved_ops.empty()) {
            std::cout << "   unresolved-go";
            for (const auto& op : h.unresolved_ops) std::cout << " " << op;
            std::cout << "\n";
        }
    }
    if (argc >= 4) {
        SessionFile sessions(argv[3]);
        int id = sessions.start("9E954", "student");
        auto resp = stand_in_response(want, 2, 1, info);
        sessions.write_response(id, resp);
        sessions.bookmark(id);
        auto back = sessions.read(id);
        auto rows = sessions.read_responses(back.file_index);
        std::cout << "session " << id << " course " << back.course
                  << " status " << back.status
                  << " responses " << rows.size()
                  << " flag " << static_cast<int>(rows.empty() ? 0 : rows[0].flag)
                  << " file " << sessions.response_path(back.file_index).filename().string()
                  << "\n";
    }
    return 0;
}
