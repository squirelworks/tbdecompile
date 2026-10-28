#include "session.hpp"

#include <chrono>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <stdexcept>

namespace fs = std::filesystem;

namespace {

void put_u16(unsigned char* p, uint16_t v) {
    p[0] = static_cast<unsigned char>(v & 0xff);
    p[1] = static_cast<unsigned char>(v >> 8);
}
void put_u32(unsigned char* p, uint32_t v) {
    put_u16(p, static_cast<uint16_t>(v & 0xffff));
    put_u16(p + 2, static_cast<uint16_t>(v >> 16));
}
uint16_t get_u16(const unsigned char* p) {
    return static_cast<uint16_t>(p[0] | (p[1] << 8));
}
uint32_t get_u32(const unsigned char* p) {
    return get_u16(p) | (static_cast<uint32_t>(get_u16(p + 2)) << 16);
}

void copy_field(char* dst, size_t n, const std::string& src) {
    std::memset(dst, 0, n);
    std::memcpy(dst, src.data(), std::min(n - 1, src.size()));
}

uint32_t ticks() {
    using namespace std::chrono;
    return static_cast<uint32_t>(duration_cast<milliseconds>(steady_clock::now().time_since_epoch()).count());
}

std::string stamp_now() {
    using namespace std::chrono;
    auto now = system_clock::now();
    std::time_t t = system_clock::to_time_t(now);
    std::tm tm{};
#if defined(_WIN32)
    localtime_s(&tm, &t);
#else
    localtime_r(&t, &tm);
#endif
    char buf[20];
    std::snprintf(buf, sizeof(buf), "%02d/%02d/%04d %02d:%02d:%02d",
                  tm.tm_mon + 1, tm.tm_mday, tm.tm_year + 1900,
                  tm.tm_hour, tm.tm_min, tm.tm_sec);
    return buf;
}

}  // namespace

void pack_session(const SessionRecord& rec, unsigned char out[kSessionSize]) {
    std::memset(out, 0, kSessionSize);
    put_u16(out + 0x00, rec.marker);
    put_u16(out + 0x02, rec.word1);
    put_u16(out + 0x04, rec.word2);
    put_u16(out + 0x06, rec.word3);
    std::memcpy(out + 0x08, rec.course, 13);
    std::memcpy(out + 0x15, rec.student, 13);
    put_u16(out + 0x22, rec.status);
    std::memcpy(out + 0x24, rec.stamp, 20);
    put_u32(out + 0x38, rec.start_tick);
    put_u32(out + 0x3c, rec.elapsed);
    put_u16(out + 0x40, rec.file_index);
    put_u32(out + 0x44, rec.tail);
}

SessionRecord unpack_session(const unsigned char in[kSessionSize]) {
    SessionRecord rec;
    rec.marker = get_u16(in + 0x00);
    rec.word1 = get_u16(in + 0x02);
    rec.word2 = get_u16(in + 0x04);
    rec.word3 = get_u16(in + 0x06);
    std::memcpy(rec.course, in + 0x08, 13);
    std::memcpy(rec.student, in + 0x15, 13);
    rec.status = get_u16(in + 0x22);
    std::memcpy(rec.stamp, in + 0x24, 20);
    rec.start_tick = get_u32(in + 0x38);
    rec.elapsed = get_u32(in + 0x3c);
    rec.file_index = get_u16(in + 0x40);
    rec.tail = get_u32(in + 0x44);
    return rec;
}

void pack_response(const ResponseRecord& rec, unsigned char out[kResponseSize]) {
    std::memset(out, 0, kResponseSize);
    put_u16(out + 0, rec.word0);
    put_u16(out + 2, rec.word1);
    put_u16(out + 4, rec.word2);
    out[6] = rec.flag;
    std::memcpy(out + 7, rec.label, 0x13);
    put_u16(out + 0x1a, rec.word3);
}

ResponseRecord unpack_response(const unsigned char in[kResponseSize]) {
    ResponseRecord rec;
    rec.word0 = get_u16(in + 0);
    rec.word1 = get_u16(in + 2);
    rec.word2 = get_u16(in + 4);
    rec.flag = in[6];
    std::memcpy(rec.label, in + 7, 0x13);
    rec.word3 = get_u16(in + 0x1a);
    return rec;
}

SessionFile::SessionFile(fs::path dir) : dir_(std::move(dir)) {
    fs::create_directories(dir_);
}

fs::path SessionFile::session_path() const { return dir_ / "SESSION3.REC"; }

fs::path SessionFile::response_path(uint16_t file_index) const {
    char name[8];
    std::snprintf(name, sizeof(name), "%03uA", static_cast<unsigned>(file_index));
    return dir_ / name;
}

int SessionFile::count() const {
    std::error_code ec;
    auto n = fs::file_size(session_path(), ec);
    if (ec) return 0;
    return static_cast<int>(n / kSessionSize);
}

int SessionFile::start(const std::string& course, const std::string& student) {
    SessionRecord rec;
    copy_field(rec.course, 13, course);
    copy_field(rec.student, 13, student);
    copy_field(rec.stamp, 20, stamp_now());
    rec.start_tick = ticks();
    int index = count();
    rec.file_index = static_cast<uint16_t>(index);
    unsigned char raw[kSessionSize];
    pack_session(rec, raw);
    std::ofstream out(session_path(), std::ios::binary | std::ios::app);
    if (!out) throw std::runtime_error("cannot write SESSION3.REC");
    out.write(reinterpret_cast<char*>(raw), kSessionSize);
    return index;
}

SessionRecord SessionFile::read(int index) const {
    std::ifstream in(session_path(), std::ios::binary);
    if (!in) throw std::runtime_error("cannot read SESSION3.REC");
    in.seekg(static_cast<std::streamoff>(index) * kSessionSize);
    unsigned char raw[kSessionSize];
    in.read(reinterpret_cast<char*>(raw), kSessionSize);
    if (in.gcount() != static_cast<std::streamsize>(kSessionSize))
        throw std::runtime_error("short SESSION3.REC record");
    return unpack_session(raw);
}

void SessionFile::write(int index, const SessionRecord& rec) {
    std::fstream io(session_path(), std::ios::binary | std::ios::in | std::ios::out);
    if (!io) throw std::runtime_error("cannot update SESSION3.REC");
    io.seekp(static_cast<std::streamoff>(index) * kSessionSize);
    unsigned char raw[kSessionSize];
    pack_session(rec, raw);
    io.write(reinterpret_cast<char*>(raw), kSessionSize);
}

void SessionFile::write_response(int index, const ResponseRecord& resp) {
    SessionRecord rec = read(index);
    uint32_t now = ticks();
    rec.elapsed = now - rec.start_tick;
    write(index, rec);
    unsigned char raw[kResponseSize];
    pack_response(resp, raw);
    std::ofstream out(response_path(rec.file_index), std::ios::binary | std::ios::app);
    if (!out) throw std::runtime_error("cannot write response file");
    out.write(reinterpret_cast<char*>(raw), kResponseSize);
}

void SessionFile::bookmark(int index) {
    SessionRecord rec = read(index);
    rec.status = 1;
    write(index, rec);
    char name[8];
    std::snprintf(name, sizeof(name), "%03uB", static_cast<unsigned>(rec.file_index));
    std::ofstream out(dir_ / name, std::ios::binary | std::ios::trunc);
    unsigned char mark[4] = {1, 0, 0, 0};
    out.write(reinterpret_cast<char*>(mark), 4);
}

std::vector<ResponseRecord> SessionFile::read_responses(uint16_t file_index) const {
    std::ifstream in(response_path(file_index), std::ios::binary);
    std::vector<ResponseRecord> out;
    if (!in) return out;
    unsigned char raw[kResponseSize];
    while (in.read(reinterpret_cast<char*>(raw), kResponseSize)) out.push_back(unpack_response(raw));
    return out;
}
