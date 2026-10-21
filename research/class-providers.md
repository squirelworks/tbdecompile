# Class providers

Segment 1278 loads class providers. A provider is a TBX DLL, a VBX DLL, a 32-bit TBX DLL, or another ToolBook book. It does not load `sysBooks`.

The provider names are stored on the book's class table. `a613` names `TB80ANM.SBK` and `TB80R.SBK`. The other sample books name none. The XML export does not record this list.

When the provider is a book, or a TBX calls `REGISTERSYSBOOK`, that book is put on a bound list. The Author program (`TB80ATH`, segment 1108) adds the bound books to `sysBooks` through `CDBADDBOUNDSYSBOOKS`, on open and when a script sets `sysBooks`.
