# 14. OpenScript bytes

## 14.1 What is current

**Known.** Handlers are compressed bytecode. The keyword pool is `TB80CMP` NE resource `0x77` (type 100, id 119). Resource `0x78` (id 120) is the other emit routine. `COMPILERPROPINFOFROMINDEX` locks resource `0x70`. Property names are a different table: BAS resource type `0x2D1`, id `0x2D0` (`bounds` `0x4004`, `idNumber` `0x4015`, `script` `0x4023`, `text` `0x402E`, `vertices` `0x4034`).

An early string dump of resource `0x77` counted 992 strings in 15776 bytes, and of `0x78` counted 980 in 15616 bytes. The decoder that actually produced the 76 Logic Families handlers counts 994 keywords. Use 994. The offset table starts at byte 2 plus count times 4. An earlier loader used count times 2 and was wrong even before the back-reference bug.

`COMPILERCOMPILETEXT` is CMP ordinal 1. `COMPILEREXPANDTEXT` is ordinal 3. `CFUNEXECUTE` is 8. `CFUNEVALUATE` is 9.

## 14.2 Encoding

From `FUN_1040_0970`. This is the encoding the handlers decode with.

| Range | Meaning |
|---|---|
| `0x00`–`0x7F` | Literal character. |
| `0x80`–`0xBF` | Keyword. Index is `byte & 0xF`, or `((byte & 0xF) << 8) \| next` when bit 4 is set. A space is appended when bit 5 is clear. |
| `0xC0`–`0xFF` | Back-reference. Copy from the compressed **input** stream, not from the output. |
| `0xE0`–`0xEF` | CRLF plus spaces. |
| `0xF0`–`0xFE` | Spaces. |
| `0xFF` | Repeat. |

The `0xC0`–`0xFF` range is also where the whitespace classes sit. The expander classifies the byte before it treats it as a generic back-reference. Do not implement "every byte above `0xBF` is a back-reference" and also implement the whitespace rows as a second pass over the same byte without the classification `FUN_1040_0970` uses.

Back-reference, as fixed on 2026-10-10:

```
if bit 4 is clear:
    length = (byte & 0xF) + 3
    src = (pos + 1) + (-4 - next_byte)
else:
    length = (byte & 0xF) + 4
    src = (pos + 1) + (-1 - word_offset)
copy `length` bytes from input[src]
```

A windowed decoder that only looks inside the slice under test will mark a back-reference that lands before the slice. On `tb80r.sbk`, reading those from the whole book dropped the `?` marks from 14256 to 66. The 66 that remain are question marks in the script.

The NIDA navigation decoder stops at the first standalone `end`. Trailing garbage is dropped. That is a corpus tool, not a claim that the expander itself stops there.

## 14.3 The superseded mismatch

`tbworkingpapers/tbwp0001/openscript_notes.md` says, in its first conclusion, that the decoder emits "italic", "third", "fourth", and "systime" where the script should say something else, and that the bytecode might not be OpenScript. That conclusion is superseded by the same file's later sections, and by this chapter.

Two bugs produced it. The keyword offset table was read as count times 2. Back-references copied from the output stream. After both fixes the same bytes are:

```
system lastbook
  lastbook = name of this book
  system nextpage
  nextpage = name of this page
  go to page "P20001" of book "nida81.tbk"
end
```

Other handlers that are real source: `send next`, `send previous`, `go to page "P400"`, `go to page "P310" of book "nida81.tbk"`.

Do not reopen "the keyword table is the wrong resource" from the early half of that note. Keywords live in `TB80CMP`. `TB80BAS` has no `handle` or `buttonClick` strings. `TB80RTM` has a small table at file `0xAACAD` (`handle`, `get`, `set`, `notifybefore`, `notifyafter`, `true`, `false`, `to`) and not the compiler keyword pool.

## 14.4 Corpus

| Book | Handlers | How they are stored |
|---|---|---|
| `9e954d01.tbk` | 76, on 39 pages | Plain `to handle` prefix, compressed body. An intermediate extract that required a plain `END` found 22. 76 is the count after the input-stream fix. |
| `nida81.tbk` | 100 | All `buttonClick`. Same encoding. |
| `tb80r.sbk` | 33 | The `to handle` / `to get` prefix is compressed too. A scan that keeps windows whose output starts with those words is how they were found. More `0xFF` and `0xE0` than the lesson books. |
| `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, `nc81trnr.sbk` | 0 decoded | High-byte runs do not decode as this bytecode. Early pattern counts (61, 17, 94, 62) were not handlers. |
| `tb80anm.sbk`, `tb80hyp.sbk` | 0 decoded | Same. Strings and menus, not this handler format. |

Of the 76 handlers in `9e954d01.tbk`, 75 are `buttonClick` and one is `EnterPage`. The 100 in `nida81.tbk` are all `buttonClick`. A handler whose name is not stored as plain text is not in those counts. The 11.5 export of `nida81.tbk` has eleven handler names. Ten of them are absent from this scan.

`openscript_analysis` `v1.0.0r9` reads this resource the same way: count at byte 0, id index, back-reference from the input, `0xFF` as a new character plus a count. It does not follow a back-reference that lands on another back-reference. The `EnterPage` handler does not need that chase. The release before it read the count from byte 2, skipped `0xC0`–`0xDF`, and repeated the previous output byte.

Lesson books store the handler name as plain text and compress the body. `tb80r.sbk` compresses the name as well. Encoding rules match. "No script at all in any system book" is too strong for `tb80r.sbk` and still true, as decoded text, for the four `nc81*` books.

## 14.5 What the courses actually do with it

The common subset is `go to`, `send`, assignment, `put into`, `set to`, `get`, increment and decrement, nested `if` / `else` / `end if`, `step from` / `to`, and `name of this book` / `this page`.

The clean-room engine also accepts `send NAME to TARGET`, a `get` that is a call, `forward to TARGET`, `break NAME`, and `PROP of TARGET`. Predicates such as `is not in` are recorded rather than evaluated. `local` and `system` declarations are ignored. Property writes are not applied to a live object. The expression evaluator copies `FUN_1008_2d31`: `+ - * /`, `abs`, `sqrt`, `log`, `exp`, `sin`, `cos`, `atan`, `asin`, `acos`, and otherwise leaves the original text. That function is not the record reader.

The page-by-page jumps are in chapter 13. Navigation is not "only a quoted page id." P20000 goes to P20001 because the handler says so.

## 14.6 Not done

A short script compiled in Instructor 8, saved, and expanded with ordinals 1 and 3 would lock the 994-name table against a known source. That test is written down and not run. Nested property expansion, opcodes past the common subset, and `forward` into a system-book handler are unimplemented or only sketched. The CMP expand host that died in `TB80W16` (`001c:00000015`, segment not present) is parked and is not the NIDA open path.
