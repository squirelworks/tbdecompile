#pragma once

#include "handler.hpp"
#include "path.hpp"

#include <string>
#include <vector>

// OpenScript engine for the handler shape we can read.
//
// A handler is source runs mixed with opcode bytes. The opcode names are
// still inside TB80CMP COMPILEREXPANDTEXT, so a byte is not given a name
// here. The engine executes the source constructs: the handler kind, a
// quoted page, and a system send. Opcode bytes are stepped and logged.
//
// buttonClick with a quoted next page goes there. buttonClick that names
// incorrectEmbedded and a retry page goes to the retry page when the
// answer is wrong. initializeTest is the shell send of that name.

struct OpcodeStep {
    unsigned char byte = 0;
    size_t offset = 0;
};

struct EngineResult {
    std::string handler;
    std::string action;
    std::string target;
    std::vector<OpcodeStep> opcodes;
    std::vector<std::string> log;
};

EngineResult run_handler(BookState& book, const Handler& handler, bool correct_answer);
EngineResult run_send(BookState& book, const std::string& name);
