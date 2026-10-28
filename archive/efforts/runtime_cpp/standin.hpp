#pragma once

#include "handler.hpp"
#include "session.hpp"

#include <string>

// What the opcode VM would have decided, and what we do instead.
//
// Known: a quoted page in a "Try Again" comment is a retry target. A quoted
// page next to a visible Go is a jump. IncorrectEmbedded / tries marks the
// page as a question. RecWriteResponse appends 0x1e bytes and does not score.
//
// Not known: which opcode operand is the right answer, and which stack word
// is the question id. The stand-in records the choice and leaves the score
// flag at 0. It does not invent a correct answer.

struct StandIn {
    bool is_question = false;
    std::vector<std::string> retry_pages;
    std::vector<std::string> go_pages;
    std::vector<std::string> unresolved;
    std::string note;
};

StandIn stand_in_for(const std::vector<Handler>& handlers);

// word0 = 1-based answer count, word1 = choice, word2 = retry targets seen,
// flag = 0 (unscored), label = page name. That is the stand-in packing of
// the six fields RecWriteResponse writes.
ResponseRecord stand_in_response(const std::string& page, uint16_t choice, uint16_t answers_so_far,
                                 const StandIn& page_info);
