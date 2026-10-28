#pragma once

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

// A handler on disk is not source and not bytecode. ASCII runs and opcode
// bytes share one stream. This splitter separates them. It does not decode
// the opcode bytes: TB80CMP still owns those names.

struct SourceRun {
    size_t offset = 0;
    std::string text;
};

struct OpcodeRun {
    size_t offset = 0;
    std::vector<unsigned char> bytes;
};

struct Handler {
    std::string kind;                 // EnterPage, buttonClick, ...
    size_t offset = 0;
    std::string source;               // ASCII runs joined
    std::vector<SourceRun> source_runs;
    std::vector<OpcodeRun> opcode_runs;
    std::vector<std::string> quotes;  // "p1082" and other quoted strings
    std::vector<std::string> comments;
    std::vector<std::string> go_pages;       // quoted page after a Go we can see
    std::vector<std::string> retry_pages;    // quoted page in a Try Again comment
    std::vector<std::string> unresolved_ops; // Go is tokenized; operand kept as hex
    bool mentions_tries = false;
    bool mentions_incorrect = false;
};

// Split one handler blob. Leading "To Handle <kind>" is required.
Handler split_handler(const unsigned char* data, size_t n, size_t file_offset = 0);

// Find handler blobs in a page record and split each one.
std::vector<Handler> split_handlers(const unsigned char* page, size_t n, size_t file_offset = 0);
