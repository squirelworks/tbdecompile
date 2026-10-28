# Viewer3

Same book XML as viewer2. New work goes here. Do not edit `viewer2/` for a viewer3 change.

Serve this folder. `viewer.html` fetches `../viewer2/course.xml` and opens each `file` relative to that catalog, so `courses/93951108.xml` is still `viewer2/courses/93951108.xml`. Opening the file directly cannot fetch the catalog.

## What still works

A viewer2 book needs no change. The frame reads the same tags `viewer2/construction.md` defines.

- Catalog: `<catalog>`, `<main>`, `<sub>`, `<course id title file>`.
- Book: `<book id title>`, `<page id n>`.
- Page children: `<p>`, `<image>`, `<go>`, `<choice>`, `<quiz>`, `<booktitle/>`.
- `go` ids `next` and `back`, and `to="last"`.
- Quiz types `choice`, `number`, `text`.
- `role="chrome"` on an image is skipped.
- Image `src` is still relative to the book file.

`kind` is still ignored.

## New files

Put a new lesson in `viewer3/courses/<id>.xml`. List it in `viewer3/extra.xml`. The frame appends that catalog after the viewer2 mains. A viewer2 book is not copied.

```xml
<main id="v3" title="Viewer3">
  <sub id="v3s0" title="New lessons">
    <course id="sample" title="Sample" file="../viewer3/courses/sample.xml"/>
  </sub>
</main>
```

`file` is resolved against `viewer2/course.xml`, so a viewer3 book uses `../viewer3/courses/...`.

## Tags viewer2 ignores

Viewer2 only draws the tags in its construction note. These are safe to add. Viewer2 skips them.

- `<note>` is a line under the page text.
- `<callout>` is a positioned label. `x` and `y` are stage pixels, same origin as `<image>`.

Do not rename a viewer2 tag. Do not put a bare `&` in the catalog.
