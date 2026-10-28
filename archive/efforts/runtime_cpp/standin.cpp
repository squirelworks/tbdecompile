#include "standin.hpp"

#include <cstring>

StandIn stand_in_for(const std::vector<Handler>& handlers) {
    StandIn s;
    for (const auto& h : handlers) {
        if (h.mentions_tries || h.mentions_incorrect) s.is_question = true;
        s.retry_pages.insert(s.retry_pages.end(), h.retry_pages.begin(), h.retry_pages.end());
        s.go_pages.insert(s.go_pages.end(), h.go_pages.begin(), h.go_pages.end());
        s.unresolved.insert(s.unresolved.end(), h.unresolved_ops.begin(), h.unresolved_ops.end());
    }
    if (s.is_question && s.unresolved.empty() && s.retry_pages.empty()) {
        s.note = "question markers, but no retry page and no tokenized Go";
    } else if (!s.unresolved.empty()) {
        s.note = "Go operand is opcode bytes; not used as a page id";
    } else if (s.is_question) {
        s.note = "retry pages come from comments; score is not in the handler text";
    } else if (!s.go_pages.empty()) {
        s.note = "quoted Go target";
    } else {
        s.note = "no navigation in the source runs";
    }
    return s;
}

ResponseRecord stand_in_response(const std::string& page, uint16_t choice, uint16_t answers_so_far,
                                 const StandIn& page_info) {
    ResponseRecord r;
    r.word0 = answers_so_far;
    r.word1 = choice;
    r.word2 = static_cast<uint16_t>(page_info.retry_pages.size());
    r.flag = 0;
    std::memset(r.label, 0, sizeof(r.label));
    std::memcpy(r.label, page.data(), std::min(sizeof(r.label) - 1, page.size()));
    r.word3 = 0;
    return r;
}
