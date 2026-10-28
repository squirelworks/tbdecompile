#include "openscript.hpp"

namespace {

std::string lower(std::string s) {
    for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    return s;
}

}  // namespace

EngineResult run_send(BookState& book, const std::string& name) {
    EngineResult result;
    result.handler = name;
    book = send(std::move(book), name);
    result.action = "send";
    result.target = name;
    result.log.push_back("send " + name);
    if (!book.log.empty()) result.log.push_back(book.log.back());
    return result;
}

EngineResult run_handler(BookState& book, const Handler& handler, bool correct_answer) {
    EngineResult result;
    result.handler = handler.kind;
    for (const auto& run : handler.opcode_runs) {
        for (unsigned char byte : run.bytes) {
            if (byte >= 0x80) result.opcodes.push_back(OpcodeStep{byte, run.offset});
        }
    }
    result.log.push_back("handler " + handler.kind + " opcodes " + std::to_string(result.opcodes.size()));

    std::string low = lower(handler.source);
    if (low.find("initializetest") != std::string::npos) {
        book = send(std::move(book), "initializeTest");
        result.action = "send";
        result.target = "initializeTest";
        result.log.push_back("initializeTest");
        return result;
    }
    if (handler.mentions_incorrect && !correct_answer && !handler.retry_pages.empty()) {
        result.action = "go";
        result.target = handler.retry_pages.front();
        if (!result.target.empty() && result.target[0] == 'p') result.target[0] = 'P';
        book = go(std::move(book), result.target);
        result.log.push_back("wrong -> " + result.target);
        return result;
    }
    std::string target;
    for (const auto& page : handler.go_pages) {
        if (handler.mentions_incorrect) continue;
        target = page;
        break;
    }
    if (target.empty() && !handler.go_pages.empty() && correct_answer) target = handler.go_pages.front();
    if (!target.empty()) {
        if (target[0] == 'p') target[0] = 'P';
        result.action = "go";
        result.target = target;
        book = go(std::move(book), target);
        result.log.push_back("go " + target);
        return result;
    }
    result.action = "stay";
    result.target = page_of(book).id;
    result.log.push_back("no source target; opcode bytes not named");
    return result;
}
