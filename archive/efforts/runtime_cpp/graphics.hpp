#pragma once

#include <cstdint>
#include <string>
#include <vector>

// Graphics the way Maybe3 paints a page.
//
// A lesson page does not keep a BM next to the widget. P400 has none.
// The placed object is the Text\0\0 property: five words, then the string.
// Maybe3/interpreter.py reads those words as x, y, w, h. reader.js scales
// the boxes onto the stage and, for a chip label, paints a body behind it.
// That body is a paintObject. It is not a bitmap.
//
// Shared chrome (the gold plate) is one carved BMP for the book, not a
// per-page widget. Draw sites are the 14 00 00 section marks Maybe3 records.

struct FieldBox {
    int x = 0;
    int y = 0;
    int w = 0;
    int h = 0;
    std::string text;
    size_t offset = 0;
    bool chip = false;
};

struct DrawSite {
    size_t offset = 0;
    unsigned char kind = 0;
};

struct PictureRef {
    bool in_page = false;
    size_t offset = 0;
    int width = 0;
    int height = 0;
    std::string note;
};

struct PageGraphic {
    std::string name;
    size_t file_offset = 0;
    std::vector<FieldBox> fields;
    std::vector<DrawSite> sites;
    PictureRef picture;
};

PageGraphic read_page_graphic(const unsigned char* page, size_t n, const std::string& name, size_t file_offset);

// Stage SVG. Coordinates are the page words, scaled the way reader.js scales.
std::string paint_svg(const PageGraphic& page, int stage_w = 900, int stage_h = 480);
