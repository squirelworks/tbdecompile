// Modern player. Not a port of TB80RTM.
//
// The 16-bit engine stays on the shelf. This binary loads a Maybe2 lesson
// shell, which already has the page graph and the quiz key, and writes one
// HTML file a 64-bit browser can open. Session recording is the 0x46 record
// from session.cpp, called by the companion tbk_path tool, not by the page.
//
//   g++ -std=c++17 -O2 -o tbk_player path.cpp session.cpp player.cpp
//   ./tbk_player lessons/9e954d01.json player.html

#include "path.hpp"

#include <fstream>
#include <iostream>
#include <sstream>

namespace {

std::string xml(const std::string& s) {
    std::string out;
    for (unsigned char c : s) {
        if (c == '&') { out.push_back('&'); out.append("amp;"); }
        else if (c == '<') { out.push_back('&'); out.append("lt;"); }
        else if (c == '>') { out.push_back('&'); out.append("gt;"); }
        else if (c == 0x22) { out.push_back('&'); out.append("quot;"); }
        else if (c >= 32 && c < 127) out.push_back(static_cast<char>(c));
    }
    return out;
}

std::string json_escape(const std::string& s) {
    std::string out;
    for (unsigned char c : s) {
        if (c == '\\' || c == '"') { out.push_back('\\'); out.push_back(static_cast<char>(c)); }
        else if (c == '\n') out.append("\\n");
        else if (c >= 32 && c < 127) out.push_back(static_cast<char>(c));
    }
    return out;
}

}  // namespace

int cmd_player(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: tbk_player <lesson.json> <out.html>\n";
        return 2;
    }
    Lesson lesson = load_lesson(argv[1]);
    BookState book = open_lesson(lesson);
    std::ostringstream html;
    html << "<!DOCTYPE html><meta charset=\"utf-8\"><title>" << xml(lesson.title) << "</title>\n"
         << "<style>body{margin:0;background:#123;color:#f4f1e8;font:16px sans-serif}"
         << "header,footer{display:flex;justify-content:space-between;padding:10px 16px;background:#0e2a4a}"
         << "main{max-width:760px;margin:24px auto;background:#1d4e89;min-height:420px;padding:28px}"
         << "button{font:14px sans-serif;margin:4px;padding:6px 12px;border:1px solid #f4f1e8;background:#fff;cursor:pointer}"
         << ".wrong{outline:2px solid #c44}</style>\n"
         << "<header><b>" << xml(lesson.title) << "</b><span id=\"count\"></span></header>\n"
         << "<main id=\"stage\"></main><footer><span id=\"nav\"></span><span id=\"score\"></span></footer>\n"
         << "<script>\nconst book = " ;
    html << "{\"id\":\"" << json_escape(lesson.id) << "\",\"title\":\"" << json_escape(lesson.title)
         << "\",\"pages\":[";
    for (size_t i = 0; i < lesson.pages.size(); ++i) {
        const auto& page = lesson.pages[i];
        if (i) html << ",";
        html << "{\"id\":\"" << json_escape(page.id) << "\",\"text\":[";
        for (size_t t = 0; t < page.text.size(); ++t) {
            if (t) html << ",";
            html << "\"" << json_escape(page.text[t]) << "\"";
        }
        html << "],\"items\":[";
        for (size_t t = 0; t < page.items.size(); ++t) {
            if (t) html << ",";
            html << "{\"label\":\"" << json_escape(page.items[t].label) << "\",\"page\":\""
                 << json_escape(page.items[t].page) << "\"}";
        }
        html << "],\"quiz\":";
        if (!page.quiz.present) html << "null";
        else {
            html << "{\"again\":\"" << json_escape(page.quiz.again) << "\",\"next\":\""
                 << json_escape(page.quiz.next) << "\",\"choices\":[";
            for (size_t t = 0; t < page.quiz.choices.size(); ++t) {
                if (t) html << ",";
                html << "{\"label\":\"" << json_escape(page.quiz.choices[t].label)
                     << "\",\"correct\":" << (page.quiz.choices[t].correct ? "true" : "false") << "}";
            }
            html << "]}";
        }
        html << "}";
    }
    html << "]};\n"
         << "let i = 0, responses = [];\n"
         << "const stage = document.getElementById('stage');\n"
         << "function score(){ const n = responses.length; const r = responses.filter(x => x.ok).length;"
         << "return n ? Math.round(100 * r / n) : 0; }\n"
         << "function go(id){ const n = book.pages.findIndex(p => p.id === id); if (n >= 0) show(n); }\n"
         << "function show(n){ i = n; const page = book.pages[i];"
         << "document.getElementById('count').textContent = page.id + '  ' + (i+1) + ' / ' + book.pages.length;"
         << "document.getElementById('score').textContent = responses.length ? ('score ' + score()) : '';"
         << "stage.replaceChildren();"
         << "for (const line of page.text){ const p = document.createElement('p'); p.textContent = line; stage.appendChild(p); }"
         << "if (page.quiz){ for (const choice of page.quiz.choices){ const b = document.createElement('button');"
         << "b.textContent = choice.label; b.onclick = () => { responses = responses.filter(x => x.page !== page.id);"
         << "responses.push({page: page.id, ok: choice.correct}); if (!choice.correct) b.className = 'wrong';"
         << "if (choice.correct && page.quiz.next) go(page.quiz.next); else if (!choice.correct && page.quiz.again) go(page.quiz.again); else show(i); };"
         << "stage.appendChild(b); } }"
         << "const nav = document.getElementById('nav'); nav.replaceChildren();"
         << "for (const item of page.items){ const b = document.createElement('button'); b.textContent = item.label;"
         << "b.onclick = () => go(item.page); nav.appendChild(b); } }\n"
         << "show(0);\n</script>\n";
    std::ofstream out(argv[2]);
    out << html.str();
    std::cout << lesson.id << " " << lesson.title
              << " pages " << lesson.pages.size()
              << " session-open " << (book.session.open ? "yes" : "no")
              << " -> " << argv[2] << "\n";
    return 0;
}
