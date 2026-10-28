#include "graphics.hpp"

#include <algorithm>
#include <cstring>
#include <sstream>

namespace {

uint16_t word_at(const unsigned char* p, size_t n, size_t off) {
    if (off + 2 > n) return 0;
    return static_cast<uint16_t>(p[off] | (p[off + 1] << 8));
}

bool chip_label(const std::string& text) {
    return text.find("74LS") != std::string::npos || text.find("MM54") != std::string::npos ||
           text.find("JL") != std::string::npos || (text.size() >= 4 && text[0] == '2' && text[1] == '7');
}

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

}  // namespace

PageGraphic read_page_graphic(const unsigned char* page, size_t n, const std::string& name, size_t file_offset) {
    PageGraphic g;
    g.name = name;
    g.file_offset = file_offset;
    const unsigned char key[] = {'T', 'e', 'x', 't', 0, 0};
    for (size_t i = 0; i + 16 < n; ++i) {
        if (std::memcmp(page + i, key, 6) != 0) continue;
        uint16_t length = word_at(page, n, i + 14);
        if (length < 8 || i + 16 + length > n) continue;
        if (page[i + 16] != 0x0d && page[i + 16] != 0x0a) continue;
        std::string text;
        for (size_t k = 0; k < length; ++k) {
            unsigned char c = page[i + 16 + k];
            if (c == '\r') continue;
            if (c == '\n') text.push_back(' ');
            else if (c >= 32 && c < 127) text.push_back(static_cast<char>(c));
        }
        while (!text.empty() && text.front() == ' ') text.erase(text.begin());
        while (!text.empty() && text.back() == ' ') text.pop_back();
        if (text.empty()) continue;
        FieldBox box;
        box.x = word_at(page, n, i + 6);
        box.y = word_at(page, n, i + 8);
        box.w = word_at(page, n, i + 12);
        box.h = word_at(page, n, i + 14);
        box.text = text;
        box.offset = i;
        box.chip = chip_label(text);
        g.fields.push_back(box);
    }
    for (size_t i = 0; i + 4 < n; ++i) {
        if (page[i] == 0x14 && page[i + 1] == 0 && page[i + 2] == 0)
            g.sites.push_back(DrawSite{i, page[i + 3]});
    }
    for (size_t i = 0; i + 14 < n; ++i) {
        if (page[i] != 'B' || page[i + 1] != 'M') continue;
        uint32_t pixel = page[i + 10] | (page[i + 11] << 8) | (page[i + 12] << 16) | (page[i + 13] << 24);
        if (pixel < 14 || i + pixel + 8 > n) continue;
        g.picture.in_page = true;
        g.picture.offset = i;
        g.picture.width = word_at(page, n, i + pixel + 4);
        g.picture.height = word_at(page, n, i + pixel + 8);
        g.picture.note = "BM in the page record";
        break;
    }
    if (!g.picture.in_page)
        g.picture.note = "no BM in the page; chip body is a paintObject anchored on the 74LS label record";
    return g;
}

std::string paint_svg(const PageGraphic& page, int stage_w, int stage_h) {
    std::ostringstream svg;
    svg << "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" << stage_w << "\" height=\"" << stage_h
        << "\" viewBox=\"0 0 " << stage_w << " " << stage_h << "\">\n";
    svg << "<rect width=\"100%\" height=\"100%\" fill=\"#1d4e89\"/>\n";
    std::vector<FieldBox> items;
    for (const auto& f : page.fields)
        if (f.w > 0 && f.h > 0) items.push_back(f);
    if (items.empty()) {
        svg << "<text x=\"24\" y=\"40\" fill=\"#f4f1e8\" font-family=\"sans-serif\" font-size=\"14\">"
            << xml(page.name) << "</text>\n</svg>\n";
        return svg.str();
    }
    int min_x = items[0].x, min_y = items[0].y, max_x = items[0].x + items[0].w, max_y = items[0].y + items[0].h;
    for (const auto& f : items) {
        min_x = std::min(min_x, f.x);
        min_y = std::min(min_y, f.y);
        max_x = std::max(max_x, f.x + f.w);
        max_y = std::max(max_y, f.y + f.h);
    }
    double scale = std::min(840.0 / std::max(1, max_x - min_x), 420.0 / std::max(1, max_y - min_y));
    auto px = [&](int x) { return 30.0 + (x - min_x) * scale; };
    auto py = [&](int y) { return 30.0 + (y - min_y) * scale; };
    for (const auto& f : items) {
        if (f.chip) {
            svg << "<rect fill=\"#111\" x=\"" << px(f.x) - 8 << "\" y=\"" << py(f.y) - 10
                << "\" width=\"" << 96 * scale << "\" height=\"" << 36 * scale << "\"/>\n";
        }
        svg << "<rect fill=\"none\" stroke=\"#f4f1e8\" x=\"" << px(f.x) << "\" y=\"" << py(f.y)
            << "\" width=\"" << std::max(f.w, 40) * scale << "\" height=\"" << std::max(f.h, 16) * scale << "\"/>\n";
        svg << "<text x=\"" << px(f.x) + 4 << "\" y=\"" << py(f.y) + 14
            << "\" fill=\"#f4f1e8\" font-family=\"sans-serif\" font-size=\"12\">" << xml(f.text.substr(0, 80))
            << "</text>\n";
    }
    svg << "</svg>\n";
    return svg.str();
}
