# Appendix E — Numeric and System Tables

Decimal/hex, ASCII, and the Win16 ordinals used when a trace names KERNEL, USER, or GDI by number.

**Date:** 16 October 2026

Decimal/hex is 0 through 255. ASCII is 0 through 127. Neither table is cut off early. The Win16 rows are the 15 October appendix, in the same order, one ordinal per row. Numbers restart at 1 for each library.

## Decimal to hexadecimal

| Dec | Hex | Dec | Hex | Dec | Hex | Dec | Hex |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 00 | 1 | 01 | 2 | 02 | 3 | 03 |
| 4 | 04 | 5 | 05 | 6 | 06 | 7 | 07 |
| 8 | 08 | 9 | 09 | 10 | 0A | 11 | 0B |
| 12 | 0C | 13 | 0D | 14 | 0E | 15 | 0F |
| 16 | 10 | 17 | 11 | 18 | 12 | 19 | 13 |
| 20 | 14 | 21 | 15 | 22 | 16 | 23 | 17 |
| 24 | 18 | 25 | 19 | 26 | 1A | 27 | 1B |
| 28 | 1C | 29 | 1D | 30 | 1E | 31 | 1F |
| 32 | 20 | 33 | 21 | 34 | 22 | 35 | 23 |
| 36 | 24 | 37 | 25 | 38 | 26 | 39 | 27 |
| 40 | 28 | 41 | 29 | 42 | 2A | 43 | 2B |
| 44 | 2C | 45 | 2D | 46 | 2E | 47 | 2F |
| 48 | 30 | 49 | 31 | 50 | 32 | 51 | 33 |
| 52 | 34 | 53 | 35 | 54 | 36 | 55 | 37 |
| 56 | 38 | 57 | 39 | 58 | 3A | 59 | 3B |
| 60 | 3C | 61 | 3D | 62 | 3E | 63 | 3F |
| 64 | 40 | 65 | 41 | 66 | 42 | 67 | 43 |
| 68 | 44 | 69 | 45 | 70 | 46 | 71 | 47 |
| 72 | 48 | 73 | 49 | 74 | 4A | 75 | 4B |
| 76 | 4C | 77 | 4D | 78 | 4E | 79 | 4F |
| 80 | 50 | 81 | 51 | 82 | 52 | 83 | 53 |
| 84 | 54 | 85 | 55 | 86 | 56 | 87 | 57 |
| 88 | 58 | 89 | 59 | 90 | 5A | 91 | 5B |
| 92 | 5C | 93 | 5D | 94 | 5E | 95 | 5F |
| 96 | 60 | 97 | 61 | 98 | 62 | 99 | 63 |
| 100 | 64 | 101 | 65 | 102 | 66 | 103 | 67 |
| 104 | 68 | 105 | 69 | 106 | 6A | 107 | 6B |
| 108 | 6C | 109 | 6D | 110 | 6E | 111 | 6F |
| 112 | 70 | 113 | 71 | 114 | 72 | 115 | 73 |
| 116 | 74 | 117 | 75 | 118 | 76 | 119 | 77 |
| 120 | 78 | 121 | 79 | 122 | 7A | 123 | 7B |
| 124 | 7C | 125 | 7D | 126 | 7E | 127 | 7F |
| 128 | 80 | 129 | 81 | 130 | 82 | 131 | 83 |
| 132 | 84 | 133 | 85 | 134 | 86 | 135 | 87 |
| 136 | 88 | 137 | 89 | 138 | 8A | 139 | 8B |
| 140 | 8C | 141 | 8D | 142 | 8E | 143 | 8F |
| 144 | 90 | 145 | 91 | 146 | 92 | 147 | 93 |
| 148 | 94 | 149 | 95 | 150 | 96 | 151 | 97 |
| 152 | 98 | 153 | 99 | 154 | 9A | 155 | 9B |
| 156 | 9C | 157 | 9D | 158 | 9E | 159 | 9F |
| 160 | A0 | 161 | A1 | 162 | A2 | 163 | A3 |
| 164 | A4 | 165 | A5 | 166 | A6 | 167 | A7 |
| 168 | A8 | 169 | A9 | 170 | AA | 171 | AB |
| 172 | AC | 173 | AD | 174 | AE | 175 | AF |
| 176 | B0 | 177 | B1 | 178 | B2 | 179 | B3 |
| 180 | B4 | 181 | B5 | 182 | B6 | 183 | B7 |
| 184 | B8 | 185 | B9 | 186 | BA | 187 | BB |
| 188 | BC | 189 | BD | 190 | BE | 191 | BF |
| 192 | C0 | 193 | C1 | 194 | C2 | 195 | C3 |
| 196 | C4 | 197 | C5 | 198 | C6 | 199 | C7 |
| 200 | C8 | 201 | C9 | 202 | CA | 203 | CB |
| 204 | CC | 205 | CD | 206 | CE | 207 | CF |
| 208 | D0 | 209 | D1 | 210 | D2 | 211 | D3 |
| 212 | D4 | 213 | D5 | 214 | D6 | 215 | D7 |
| 216 | D8 | 217 | D9 | 218 | DA | 219 | DB |
| 220 | DC | 221 | DD | 222 | DE | 223 | DF |
| 224 | E0 | 225 | E1 | 226 | E2 | 227 | E3 |
| 228 | E4 | 229 | E5 | 230 | E6 | 231 | E7 |
| 232 | E8 | 233 | E9 | 234 | EA | 235 | EB |
| 236 | EC | 237 | ED | 238 | EE | 239 | EF |
| 240 | F0 | 241 | F1 | 242 | F2 | 243 | F3 |
| 244 | F4 | 245 | F5 | 246 | F6 | 247 | F7 |
| 248 | F8 | 249 | F9 | 250 | FA | 251 | FB |
| 252 | FC | 253 | FD | 254 | FE | 255 | FF |

## ASCII (0–127)

Controls are shown by name. The landscape one-page card remains `TBdecompile/ASCII_lookup.pdf`.

| Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 00 | NUL | 1 | 01 | SOH | 2 | 02 | STX | 3 | 03 | ETX |
| 4 | 04 | EOT | 5 | 05 | ENQ | 6 | 06 | ACK | 7 | 07 | BEL |
| 8 | 08 | BS | 9 | 09 | HT | 10 | 0A | LF | 11 | 0B | VT |
| 12 | 0C | FF | 13 | 0D | CR | 14 | 0E | SO | 15 | 0F | SI |
| 16 | 10 | DLE | 17 | 11 | DC1 | 18 | 12 | DC2 | 19 | 13 | DC3 |
| 20 | 14 | DC4 | 21 | 15 | NAK | 22 | 16 | SYN | 23 | 17 | ETB |
| 24 | 18 | CAN | 25 | 19 | EM | 26 | 1A | SUB | 27 | 1B | ESC |
| 28 | 1C | FS | 29 | 1D | GS | 30 | 1E | RS | 31 | 1F | US |
| 32 | 20 | SP | 33 | 21 | ! | 34 | 22 | " | 35 | 23 | # |
| 36 | 24 | $ | 37 | 25 | % | 38 | 26 | & | 39 | 27 | ' |
| 40 | 28 | ( | 41 | 29 | ) | 42 | 2A | * | 43 | 2B | + |
| 44 | 2C | , | 45 | 2D | - | 46 | 2E | . | 47 | 2F | / |
| 48 | 30 | 0 | 49 | 31 | 1 | 50 | 32 | 2 | 51 | 33 | 3 |
| 52 | 34 | 4 | 53 | 35 | 5 | 54 | 36 | 6 | 55 | 37 | 7 |
| 56 | 38 | 8 | 57 | 39 | 9 | 58 | 3A | : | 59 | 3B | ; |
| 60 | 3C | < | 61 | 3D | = | 62 | 3E | > | 63 | 3F | ? |
| 64 | 40 | @ | 65 | 41 | A | 66 | 42 | B | 67 | 43 | C |
| 68 | 44 | D | 69 | 45 | E | 70 | 46 | F | 71 | 47 | G |
| 72 | 48 | H | 73 | 49 | I | 74 | 4A | J | 75 | 4B | K |
| 76 | 4C | L | 77 | 4D | M | 78 | 4E | N | 79 | 4F | O |
| 80 | 50 | P | 81 | 51 | Q | 82 | 52 | R | 83 | 53 | S |
| 84 | 54 | T | 85 | 55 | U | 86 | 56 | V | 87 | 57 | W |
| 88 | 58 | X | 89 | 59 | Y | 90 | 5A | Z | 91 | 5B | [ |
| 92 | 5C | \ | 93 | 5D | ] | 94 | 5E | ^ | 95 | 5F | _ |
| 96 | 60 | ` | 97 | 61 | a | 98 | 62 | b | 99 | 63 | c |
| 100 | 64 | d | 101 | 65 | e | 102 | 66 | f | 103 | 67 | g |
| 104 | 68 | h | 105 | 69 | i | 106 | 6A | j | 107 | 6B | k |
| 108 | 6C | l | 109 | 6D | m | 110 | 6E | n | 111 | 6F | o |
| 112 | 70 | p | 113 | 71 | q | 114 | 72 | r | 115 | 73 | s |
| 116 | 74 | t | 117 | 75 | u | 118 | 76 | v | 119 | 77 | w |
| 120 | 78 | x | 121 | 79 | y | 122 | 7A | z | 123 | 7B | { |
| 124 | 7C | vertical bar | 125 | 7D | } | 126 | 7E | ~ | 127 | 7F | DEL |

## Win16 system ordinals

| Library | Ordinal | Name |
| --- | --- | --- |
| KERNEL | 1 | InitTask |
| KERNEL | 2 | ExitWindows |
| KERNEL | 3 | WaitEvent |
| KERNEL | 4 | PostEvent |
| KERNEL | 5 | SetPriority |
| KERNEL | 6 | LockCurrentTask |
| KERNEL | 7 | UnlockCurrentTask |
| KERNEL | 8 | GetCurrentTask |
| KERNEL | 9 | GetCurrentPDB |
| KERNEL | 10 | GetDOSEnvironment |
| KERNEL | 11 | GetInstanceData |
| KERNEL | 12 | SetInstanceData |
| KERNEL | 13 | GetExePtr |
| KERNEL | 14 | GetProcAddress |
| KERNEL | 15 | MakeProcInstance |
| KERNEL | 16 | FreeProcInstance |
| KERNEL | 17 | GetModuleHandle |
| KERNEL | 18 | GetModuleUsage |
| KERNEL | 19 | GetModuleFileName |
| KERNEL | 20 | GetWindowsDirectory |
| KERNEL | 21 | GetSystemDirectory |
| KERNEL | 22 | GetFreeSpace |
| KERNEL | 23 | GetTempDrive |
| KERNEL | 24 | GetTempFileName |
| KERNEL | 25 | Catch |
| KERNEL | 26 | Throw |
| KERNEL | 27 | LocalAlloc |
| KERNEL | 28 | LocalReAlloc |
| KERNEL | 29 | LocalFree |
| KERNEL | 30 | LocalLock |
| KERNEL | 31 | LocalUnlock |
| KERNEL | 32 | LocalSize |
| KERNEL | 33 | LocalFlags |
| KERNEL | 34 | LocalCompact |
| KERNEL | 35 | LocalNotify |
| KERNEL | 36 | GlobalAlloc |
| KERNEL | 37 | GlobalReAlloc |
| KERNEL | 38 | GlobalFree |
| KERNEL | 39 | GlobalLock |
| KERNEL | 40 | GlobalUnlock |
| USER | 1 | MessageBox |
| USER | 2 | GetFocus |
| USER | 3 | SetFocus |
| USER | 4 | GetActiveWindow |
| USER | 5 | SetActiveWindow |
| USER | 6 | GetCapture |
| USER | 7 | SetCapture |
| USER | 8 | ReleaseCapture |
| USER | 9 | GetWindowTask |
| USER | 10 | IsWindow |
| USER | 11 | IsChild |
| USER | 12 | IsWindowVisible |
| USER | 13 | IsWindowEnabled |
| USER | 14 | IsIconic |
| USER | 15 | IsZoomed |
| USER | 16 | ClientToScreen |
| USER | 17 | ScreenToClient |
| USER | 18 | WindowFromPoint |
| USER | 19 | ChildWindowFromPoint |
| USER | 20 | GetWindowWord |
| USER | 21 | SetWindowWord |
| USER | 22 | GetWindowLong |
| USER | 23 | SetWindowLong |
| USER | 24 | GetClassWord |
| USER | 25 | SetClassWord |
| USER | 26 | GetClassLong |
| USER | 27 | SetClassLong |
| USER | 28 | GetDesktopWindow |
| USER | 29 | GetParent |
| USER | 30 | SetParent |
| USER | 31 | GetWindow |
| USER | 32 | GetNextWindow |
| USER | 33 | GetTopWindow |
| USER | 34 | GetWindowText |
| USER | 35 | SetWindowText |
| USER | 36 | GetWindowTextLength |
| USER | 37 | GetClientRect |
| USER | 38 | GetWindowRect |
| USER | 39 | AdjustWindowRect |
| USER | 40 | AdjustWindowRectEx |
| GDI | 1 | GetStockObject |
| GDI | 2 | SelectObject |
| GDI | 3 | DeleteObject |
| GDI | 4 | GetObject |
| GDI | 5 | GetCurrentObject |
| GDI | 6 | UnrealizeObject |
| GDI | 7 | CreatePen |
| GDI | 8 | CreatePenIndirect |
| GDI | 9 | CreateSolidBrush |
| GDI | 10 | CreateHatchBrush |
| GDI | 11 | CreatePatternBrush |
| GDI | 12 | CreateBrushIndirect |
| GDI | 13 | CreateBitmap |
| GDI | 14 | CreateBitmapIndirect |
| GDI | 15 | CreateCompatibleBitmap |
| GDI | 16 | CreateDiscardableBitmap |
| GDI | 17 | CreateDIBitmap |
| GDI | 18 | CreateDIBPatternBrush |
| GDI | 19 | GetBitmapBits |
| GDI | 20 | SetBitmapBits |
| GDI | 21 | GetBitmapDimension |
| GDI | 22 | SetBitmapDimension |
| GDI | 23 | GetTextExtent |
| GDI | 24 | GetTextExtentEx |
| GDI | 25 | GetTabbedTextExtent |
| GDI | 26 | TabbedTextOut |
| GDI | 27 | ExtTextOut |
| GDI | 28 | TextOut |
| GDI | 29 | GetTextMetrics |
| GDI | 30 | GetTextFace |
| GDI | 31 | GetTextAlign |
| GDI | 32 | SetTextAlign |
| GDI | 33 | GetTextCharacterExtra |
| GDI | 34 | SetTextCharacterExtra |
| GDI | 35 | GetTextColor |
| GDI | 36 | SetTextColor |
| GDI | 37 | GetBkColor |
| GDI | 38 | SetBkColor |
| GDI | 39 | GetBkMode |
| GDI | 40 | SetBkMode |
