#pragma once

#include <cstdint>
#include <filesystem>
#include <string>
#include <vector>

// SESSION3.REC as nc81rec.dll writes it.
//
// FUN_10001060 / FUN_10001140 move one 0x46-byte record. RecStartSession
// indexes the file by record * 0x46. RecWriteResponse rewrites that record
// (elapsed = now - start tick) and appends 0x1e bytes to the response file.
//
// Response filename: FUN_10001610 zero-pads the record's file index to 3
// digits and appends the suffix at DAT_10009080, which is the byte 'A'.
// Bookmark suffix at DAT_100090ac is 'B'. The directory comes from
// NIDAREC.INI RecordPath; that ini is not in the lesson, so the caller
// passes the directory.

constexpr size_t kSessionSize = 0x46;
constexpr size_t kResponseSize = 0x1e;

struct SessionRecord {
    uint16_t marker = 1;       // reader rejects a record whose first word is not 1
    uint16_t word1 = 0;
    uint16_t word2 = 1;
    uint16_t word3 = 0;
    char course[13] = {};
    char student[13] = {};
    uint16_t status = 0;       // 0 open, 1 bookmarked (RecCheckStatus)
    char stamp[20] = {};       // 20-byte field; DLL formats are %02d/%02d/%04d and %02d:%02d:%02d
    uint32_t start_tick = 0;
    uint32_t elapsed = 0;
    uint16_t file_index = 0;   // argument to the response-name builder
    uint32_t tail = 0;
};

struct ResponseRecord {
    uint16_t word0 = 0;        // written from the call stack; meaning not recovered
    uint16_t word1 = 0;
    uint16_t word2 = 0;
    uint8_t flag = 0;
    char label[0x13] = {};
    uint16_t word3 = 0;
};

class SessionFile {
public:
    explicit SessionFile(std::filesystem::path dir);

    // Append one session. Returns the record index RecStartSession would hand back.
    int start(const std::string& course, const std::string& student);
    SessionRecord read(int index) const;
    void write(int index, const SessionRecord& rec);
    int count() const;

    // RecWriteResponse: refresh elapsed, then append the 0x1e response.
    void write_response(int index, const ResponseRecord& resp);
    // RecBookmarkSession sets status to 1 and writes the 'B' sibling.
    void bookmark(int index);

    std::filesystem::path session_path() const;
    std::filesystem::path response_path(uint16_t file_index) const;
    std::vector<ResponseRecord> read_responses(uint16_t file_index) const;

private:
    std::filesystem::path dir_;
};

void pack_session(const SessionRecord& rec, unsigned char out[kSessionSize]);
SessionRecord unpack_session(const unsigned char in[kSessionSize]);
void pack_response(const ResponseRecord& rec, unsigned char out[kResponseSize]);
ResponseRecord unpack_response(const unsigned char in[kResponseSize]);
