# Appendix D — Address Maps

NE segment to Ghidra space, and one boot's WDW selectors.

**Date:** 16 October 2026

Each map below is the current file, complete. NE segment numbers are not Ghidra `CodeN` names. Segment 1 is `1000`, segment 2 is `1008`, and the usual step is 8, with gaps. Live selectors change every boot. Offsets inside a segment do not. The symbol maps are not reprinted. They are unsifted decompiler names and were removed from this edition. They remain on disk under `TBdecompile/20261015/20261012/`.



# NE segment to Ghidra address

> Trail, 2026-10-16. Lookup. NE segment to the Ghidra base used for this load. Not a finding. A live selector is not this base. If this file and `TBdecompile/record/` disagree, the record wins.

NE segment number, file offset, length, and flags were checked against the unpacked binaries in `Toolbook/_unpacked`. They match, file for file, including BAS (199) and RTM (139).

The Ghidra base is not stored in the DLL. It is `0x1000 + (NE - 1) * 8`, and the block is `CodeN` or `DataN`. That is how these listings were loaded. The DLL confirms the segment index. The listing confirms the address Ghidra gave it.

A listing address `Code35:1110:04e8` is NE segment 35, offset `0x04E8`.

`tbwp0023/rtm-ne-to-ghidra.md` drifts by 8 bytes at NE `0x2D`. The binary and the RTM `-5` listing both have `Code45:1160`.

`TB80OLE.DLL` is in this table from the unpacked binary. Its HTML export is one raw block (`CODE_0:1000`) and has no segment table. The Ghidra names for OLE follow the same formula. They have not been seen in a listing.

`TB80ATH.EXE`, `DIBUTIL.DLL`, and `decrypt.exe` are listing-only. Those three binaries are not in `_unpacked`.

OCX segments 50 and 51 have file offset 0 and a length word of 0. Minimum allocation is `0x0E`. There are no file bytes. That is not a 64K segment.

PE files, no NE table: `TB80ACX`, `TB80ENU2`, `TB80F32L`, `TB80MAIN`, `TB80RMT`, `TB80RUN`, `TB80W32`, `Tbload`, `zlib1`.

## Index

| File | Segments | Entry | Auto data | Data segments | Source |
|---|---:|---|---|---|---|
| DIBUTIL.DLL.html | 5 | NE 2 → `1008:961E` | NE 5 → `1020` | 4,5 | listing only |
| TB80ATH.EXE.html | 184 | NE 2 → `1008:063A` | NE 184 → `15B8` | 184 | listing only |
| TB80BAS.DLL-4.html | 199 | NE 2 → `1008:089E` | NE 199 → `1630` | 193,194,195,196,197,198,199 | DLL matches listing |
| TB80BMP.DLL.html | 27 | NE 2 → `1008:02D8` | NE 27 → `10D0` | 26,27 | DLL matches listing |
| TB80CMP.ghidra.dll.html | 47 | NE 2 → `1008:00BE` | NE 47 → `1170` | 35,36,37,38,39,40,41,42,43,44,45,46,47 | DLL matches listing |
| TB80ENU1.DLL.html | 8 | NE 6 → `1028:0054` | NE 8 → `1038` | 8 | DLL matches listing |
| TB80FLT.DLL.html | 28 | NE 23 → `10B0:0484` | NE 28 → `10D8` | 27,28 | DLL matches listing |
| TB80JPG.DLL.html | 3 | NE 2 → `1008:A5C2` | NE 3 → `1010` | 3 | DLL matches listing |
| TB80LNL.DLL.html | 39 | NE 15 → `1070:0054` | NE 39 → `1130` | 37,38,39 | DLL matches listing |
| TB80MM.DLL.html | 22 | NE 3 → `1010:0054` | NE 22 → `10A8` | 22 | DLL matches listing |
| TB80NET.EXE.html | 45 | NE 2 → `1008:0120` | NE 45 → `1160` | 44,45 | DLL matches listing |
| TB80OCX.DLL.html | 53 | NE 1 → `1000:0054` | NE 53 → `11A0` | 47,48,49,50,51,52,53 | DLL matches listing |
| TB80RCR.DLL.html | 5 | NE 2 → `1008:A998` | NE 5 → `1020` | 4,5 | DLL matches listing |
| TB80RTM.EXE-5.html | 139 | NE 2 → `1008:035A` | NE 139 → `1450` | 139 | DLL matches listing |
| TB80UTL.DLL.html | 32 | NE 4 → `1018:0526` | NE 32 → `10F8` | 30,31,32 | DLL matches listing |
| TB80VBX.DLL.html | 47 | NE 2 → `1008:00DA` | NE 47 → `1170` | 47 | DLL matches listing |
| TB80W16.DLL.html | 56 | NE 3 → `1010:027A` | NE 56 → `11B8` | 35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56 | DLL matches listing |
| TBCBT.DLL.html | 16 | NE 2 → `1008:0054` | NE 16 → `1078` | 16 | DLL matches listing |
| TBDB3.DLL.html | 72 | NE 2 → `1008:0628` | NE 72 → `1238` | 70,71,72 | DLL matches listing |
| TBDLG.DLL.html | 19 | NE 17 → `1080:027A` | NE 19 → `1090` | 19 | DLL matches listing |
| TBDOS.DLL.html | 7 | NE 2 → `1008:027A` | NE 7 → `1030` | 7 | DLL matches listing |
| TBFILE32.DLL.html | 9 | NE 3 → `1010:0054` | NE 9 → `1040` | 9 | DLL matches listing |
| TBPDX.DLL.html | 5 | NE 4 → `1018:0068` | NE 5 → `1020` | 5 | DLL matches listing |
| TBREG.DLL.html | 11 | NE 2 → `1008:0064` | NE 11 → `1050` | 11 | DLL matches listing |
| TBWIN.DLL.html | 28 | NE 2 → `1008:0946` | NE 28 → `10D8` | 28 | DLL matches listing |
| decrypt.exe.html | 3 | NE 2 → `1008:15A4` | NE 3 → `1010` | 3 | listing only |
| TB80OLE.DLL | 32 | NE 2 → `1008:0054` | NE 32 → `10F8` | 31,32 | DLL only |

## DIBUTIL.DLL.html

Entry NE 2 at `1008:961E`. Auto data NE 5 at `1020`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x440` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xE50` | `0xC3C9` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0xDC50` | `0x6930` | `0x1D50` |
| 4 (`0x04`) | `Data4:1018` | Data | `0x14950` | `0x16` | `0x0C71` |
| 5 (`0x05`) | `Data5:1020` | Data | `0x14970` | `0x3478` | `0x0D71` |

## TB80ATH.EXE.html

Entry NE 2 at `1008:063A`. Auto data NE 184 at `15B8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x1F60` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x2980` | `0x6800` | `0x0D40` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x9B00` | `0x1F50` | `0x1D50` |
| 4 (`0x04`) | `Code4:1018` | Code | `0xBC60` | `0x2B2E` | `0x1D50` |
| 5 (`0x05`) | `Code5:1020` | Code | `0xEA00` | `0x30C8` | `0x1D50` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x11D20` | `0x55E` | `0x1D50` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x122A0` | `0x50C` | `0x1D50` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x12880` | `0x38A` | `0x1D50` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x12CC0` | `0x9EE` | `0x1D50` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x13780` | `0x792` | `0x1D50` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x14060` | `0x1A92` | `0x1D50` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x15C20` | `0xAF4` | `0x1D50` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x168A0` | `0x1A46` | `0x1D50` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x18600` | `0x430` | `0x1D50` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x18AE0` | `0x21C4` | `0x1D50` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x1AFA0` | `0x1E96` | `0x1D50` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x1D040` | `0xEE4` | `0x1D50` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x1E060` | `0x3D2` | `0x1D50` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x1E4A0` | `0x638` | `0x1D50` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x1EB80` | `0x314A` | `0x1D50` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x220E0` | `0x1066` | `0x1D50` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x23240` | `0x250A` | `0x1D50` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x25A80` | `0x340C` | `0x1D50` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x29020` | `0x359E` | `0x1D50` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x2C8A0` | `0x36CA` | `0x1D50` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x30340` | `0x22A6` | `0x1D50` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x32720` | `0x1EC` | `0x1D50` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x329A0` | `0x3558` | `0x1D50` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x36160` | `0x47E` | `0x1D50` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x366A0` | `0xEAA` | `0x1D50` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x376E0` | `0x153C` | `0x1D50` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x38DC0` | `0x2200` | `0x1D50` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x3B340` | `0x5272` | `0x1D50` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x408A0` | `0x994` | `0x1D50` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x41320` | `0x994` | `0x1D50` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x41D60` | `0x59F8` | `0x1D50` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x479A0` | `0x3DE` | `0x1D50` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x47DE0` | `0x127A` | `0x1D50` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x49200` | `0x102A` | `0x1D50` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x4A360` | `0x4134` | `0x1D50` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x4E680` | `0x1A1A` | `0x1D50` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x501A0` | `0xB5A` | `0x1D50` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x50DC0` | `0x67A` | `0x1D50` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0x514A0` | `0x258` | `0x1D50` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0x51720` | `0x101A` | `0x1D50` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0x527E0` | `0x1E68` | `0x1C50` |
| 47 (`0x2F`) | `Code47:1170` | Code | `0x54660` | `0x15BC` | `0x1D50` |
| 48 (`0x30`) | `Code48:1178` | Code | `0x55EA0` | `0x1394` | `0x1D50` |
| 49 (`0x31`) | `Code49:1180` | Code | `0x57360` | `0x15E4` | `0x1D50` |
| 50 (`0x32`) | `Code50:1188` | Code | `0x58B40` | `0x1B84` | `0x1D50` |
| 51 (`0x33`) | `Code51:1190` | Code | `0x5A960` | `0x1486` | `0x1D50` |
| 52 (`0x34`) | `Code52:1198` | Code | `0x5BF20` | `0x2C58` | `0x1D50` |
| 53 (`0x35`) | `Code53:11A0` | Code | `0x5EF00` | `0x1AE0` | `0x1D50` |
| 54 (`0x36`) | `Code54:11A8` | Code | `0x60B40` | `0xCE2` | `0x1D50` |
| 55 (`0x37`) | `Code55:11B0` | Code | `0x61960` | `0xFAE` | `0x1D50` |
| 56 (`0x38`) | `Code56:11B8` | Code | `0x62AC0` | `0x17A4` | `0x1D50` |
| 57 (`0x39`) | `Code57:11C0` | Code | `0x64300` | `0x50E` | `0x1D50` |
| 58 (`0x3A`) | `Code58:11C8` | Code | `0x648A0` | `0x5EC` | `0x1D50` |
| 59 (`0x3B`) | `Code59:11D0` | Code | `0x64EC0` | `0x84` | `0x1D50` |
| 60 (`0x3C`) | `Code60:11D8` | Code | `0x64F60` | `0x854` | `0x1D50` |
| 61 (`0x3D`) | `Code61:11E0` | Code | `0x658E0` | `0xC84` | `0x1D50` |
| 62 (`0x3E`) | `Code62:11E8` | Code | `0x66660` | `0x196E` | `0x1D10` |
| 63 (`0x3F`) | `Code63:11F0` | Code | `0x68180` | `0x2FF8` | `0x1D10` |
| 64 (`0x40`) | `Code64:11F8` | Code | `0x6B500` | `0x39B2` | `0x1D10` |
| 65 (`0x41`) | `Code65:1200` | Code | `0x6F240` | `0x2CB8` | `0x1D10` |
| 66 (`0x42`) | `Code66:1208` | Code | `0x72220` | `0x214` | `0x1D10` |
| 67 (`0x43`) | `Code67:1210` | Code | `0x724A0` | `0x850` | `0x1D10` |
| 68 (`0x44`) | `Code68:1218` | Code | `0x72DC0` | `0x16A` | `0x1D10` |
| 69 (`0x45`) | `Code69:1220` | Code | `0x72F80` | `0x1674` | `0x1D10` |
| 70 (`0x46`) | `Code70:1228` | Code | `0x74760` | `0x50A` | `0x1D10` |
| 71 (`0x47`) | `Code71:1230` | Code | `0x74D40` | `0xF46` | `0x1D10` |
| 72 (`0x48`) | `Code72:1238` | Code | `0x75DC0` | `0xC04` | `0x1D10` |
| 73 (`0x49`) | `Code73:1240` | Code | `0x76AA0` | `0x22` | `0x1D10` |
| 74 (`0x4A`) | `Code74:1248` | Code | `0x76AE0` | `0x4E6` | `0x1D10` |
| 75 (`0x4B`) | `Code75:1250` | Code | `0x77080` | `0x3240` | `0x1D10` |
| 76 (`0x4C`) | `Code76:1258` | Code | `0x7A4A0` | `0x71E` | `0x1D10` |
| 77 (`0x4D`) | `Code77:1260` | Code | `0x7AD20` | `0xD8C` | `0x1D10` |
| 78 (`0x4E`) | `Code78:1268` | Code | `0x7BC00` | `0x6D94` | `0x1D10` |
| 79 (`0x4F`) | `Code79:1270` | Code | `0x82D20` | `0x4C` | `0x1D10` |
| 80 (`0x50`) | `Code80:1278` | Code | `0x82D80` | `0x1B0` | `0x1D10` |
| 81 (`0x51`) | `Code81:1280` | Code | `0x82F60` | `0x496` | `0x1D10` |
| 82 (`0x52`) | `Code82:1288` | Code | `0x83440` | `0xACE` | `0x1D10` |
| 83 (`0x53`) | `Code83:1290` | Code | `0x83FA0` | `0xC7E` | `0x1D10` |
| 84 (`0x54`) | `Code84:1298` | Code | `0x84D80` | `0x2AEA` | `0x1D10` |
| 85 (`0x55`) | `Code85:12A0` | Code | `0x87C60` | `0x2638` | `0x1D10` |
| 86 (`0x56`) | `Code86:12A8` | Code | `0x8A4E0` | `0x11DE` | `0x1D10` |
| 87 (`0x57`) | `Code87:12B0` | Code | `0x8B840` | `0x372E` | `0x1D10` |
| 88 (`0x58`) | `Code88:12B8` | Code | `0x8F2A0` | `0x8EE0` | `0x1D10` |
| 89 (`0x59`) | `Code89:12C0` | Code | `0x98700` | `0x2088` | `0x1D10` |
| 90 (`0x5A`) | `Code90:12C8` | Code | `0x9A9A0` | `0xD28` | `0x1D10` |
| 91 (`0x5B`) | `Code91:12D0` | Code | `0x9B7C0` | `0x32E` | `0x1D10` |
| 92 (`0x5C`) | `Code92:12D8` | Code | `0x9BB60` | `0x17F0` | `0x1D10` |
| 93 (`0x5D`) | `Code93:12E0` | Code | `0x9D400` | `0x1B00` | `0x1D10` |
| 94 (`0x5E`) | `Code94:12E8` | Code | `0x9F060` | `0xA80` | `0x1D10` |
| 95 (`0x5F`) | `Code95:12F0` | Code | `0x9FBC0` | `0xBE2` | `0x1D10` |
| 96 (`0x60`) | `Code96:12F8` | Code | `0xA0820` | `0x35A8` | `0x1D10` |
| 97 (`0x61`) | `Code97:1300` | Code | `0xA4020` | `0x1822` | `0x1D10` |
| 98 (`0x62`) | `Code98:1308` | Code | `0xA59C0` | `0x592` | `0x1D10` |
| 99 (`0x63`) | `Code99:1310` | Code | `0xA5FA0` | `0x96E` | `0x1D10` |
| 100 (`0x64`) | `Code100:1318` | Code | `0xA69C0` | `0x138` | `0x1D10` |
| 101 (`0x65`) | `Code101:1320` | Code | `0xA6B40` | `0x14E` | `0x1D10` |
| 102 (`0x66`) | `Code102:1328` | Code | `0xA6CE0` | `0x5BE` | `0x1D10` |
| 103 (`0x67`) | `Code103:1330` | Code | `0xA7320` | `0x6C6` | `0x1D10` |
| 104 (`0x68`) | `Code104:1338` | Code | `0xA7AC0` | `0x464` | `0x1C10` |
| 105 (`0x69`) | `Code105:1340` | Code | `0xA7F40` | `0x75E` | `0x1D10` |
| 106 (`0x6A`) | `Code106:1348` | Code | `0xA8720` | `0x784` | `0x1D10` |
| 107 (`0x6B`) | `Code107:1350` | Code | `0xA8EE0` | `0xD9E` | `0x1D10` |
| 108 (`0x6C`) | `Code108:1358` | Code | `0xA9D80` | `0x258` | `0x1D10` |
| 109 (`0x6D`) | `Code109:1360` | Code | `0xAA020` | `0x1EF0` | `0x1D10` |
| 110 (`0x6E`) | `Code110:1368` | Code | `0xAC120` | `0xC4C` | `0x1D10` |
| 111 (`0x6F`) | `Code111:1370` | Code | `0xACE40` | `0x2308` | `0x1D10` |
| 112 (`0x70`) | `Code112:1378` | Code | `0xAF880` | `0xDAA` | `0x1D10` |
| 113 (`0x71`) | `Code113:1380` | Code | `0xB0700` | `0xAE` | `0x1D10` |
| 114 (`0x72`) | `Code114:1388` | Code | `0xB07C0` | `0x7FA` | `0x1D10` |
| 115 (`0x73`) | `Code115:1390` | Code | `0xB1040` | `0x38D0` | `0x1D10` |
| 116 (`0x74`) | `Code116:1398` | Code | `0xB5FC0` | `0x22E0` | `0x1D10` |
| 117 (`0x75`) | `Code117:13A0` | Code | `0xB8460` | `0x854` | `0x1D10` |
| 118 (`0x76`) | `Code118:13A8` | Code | `0xB8D60` | `0x91A` | `0x1D10` |
| 119 (`0x77`) | `Code119:13B0` | Code | `0xB9780` | `0x19B6` | `0x1D10` |
| 120 (`0x78`) | `Code120:13B8` | Code | `0xBB340` | `0x1A70` | `0x1D10` |
| 121 (`0x79`) | `Code121:13C0` | Code | `0xBCFC0` | `0x118` | `0x1D10` |
| 122 (`0x7A`) | `Code122:13C8` | Code | `0xBD120` | `0x2E` | `0x1C10` |
| 123 (`0x7B`) | `Code123:13D0` | Code | `0xBD160` | `0xB1A` | `0x1D10` |
| 124 (`0x7C`) | `Code124:13D8` | Code | `0xBDD60` | `0xFCA` | `0x1D10` |
| 125 (`0x7D`) | `Code125:13E0` | Code | `0xBEE40` | `0x1510` | `0x1D10` |
| 126 (`0x7E`) | `Code126:13E8` | Code | `0xC0560` | `0xE0A` | `0x1D10` |
| 127 (`0x7F`) | `Code127:13F0` | Code | `0xC15A0` | `0xD54` | `0x1D10` |
| 128 (`0x80`) | `Code128:13F8` | Code | `0xC2400` | `0xA84` | `0x1D10` |
| 129 (`0x81`) | `Code129:1400` | Code | `0xC2F80` | `0x1E8` | `0x1D10` |
| 130 (`0x82`) | `Code130:1408` | Code | `0xC31E0` | `0x56C` | `0x1D10` |
| 131 (`0x83`) | `Code131:1410` | Code | `0xC3820` | `0x2D8` | `0x1D10` |
| 132 (`0x84`) | `Code132:1418` | Code | `0xC3B80` | `0x5A0` | `0x1D10` |
| 133 (`0x85`) | `Code133:1420` | Code | `0xC4220` | `0x122A` | `0x1D10` |
| 134 (`0x86`) | `Code134:1428` | Code | `0xC56A0` | `0x63A` | `0x1D10` |
| 135 (`0x87`) | `Code135:1430` | Code | `0xC5D40` | `0x1A98` | `0x1D10` |
| 136 (`0x88`) | `Code136:1438` | Code | `0xC7980` | `0x498` | `0x1D10` |
| 137 (`0x89`) | `Code137:1440` | Code | `0xC7E80` | `0xF2E` | `0x1D10` |
| 138 (`0x8A`) | `Code138:1448` | Code | `0xC8E60` | `0x396` | `0x1D10` |
| 139 (`0x8B`) | `Code139:1450` | Code | `0xC9260` | `0x197A` | `0x1D10` |
| 140 (`0x8C`) | `Code140:1458` | Code | `0xCAE80` | `0x720` | `0x1D10` |
| 141 (`0x8D`) | `Code141:1460` | Code | `0xCB700` | `0x140` | `0x1D10` |
| 142 (`0x8E`) | `Code142:1468` | Code | `0xCB880` | `0x136` | `0x1D10` |
| 143 (`0x8F`) | `Code143:1470` | Code | `0xCBA00` | `0x1D4` | `0x1D10` |
| 144 (`0x90`) | `Code144:1478` | Code | `0xCBC00` | `0xDF8` | `0x1D10` |
| 145 (`0x91`) | `Code145:1480` | Code | `0xCCAA0` | `0x9F2` | `0x1D10` |
| 146 (`0x92`) | `Code146:1488` | Code | `0xCD560` | `0xA4A` | `0x1D10` |
| 147 (`0x93`) | `Code147:1490` | Code | `0xCE040` | `0xCBE` | `0x1D10` |
| 148 (`0x94`) | `Code148:1498` | Code | `0xCEDA0` | `0x48C` | `0x1D10` |
| 149 (`0x95`) | `Code149:14A0` | Code | `0xCF240` | `0x8B6` | `0x1D10` |
| 150 (`0x96`) | `Code150:14A8` | Code | `0xCFB60` | `0xC34` | `0x1D10` |
| 151 (`0x97`) | `Code151:14B0` | Code | `0xD0820` | `0x112` | `0x1D10` |
| 152 (`0x98`) | `Code152:14B8` | Code | `0xD0980` | `0x9BC` | `0x1D10` |
| 153 (`0x99`) | `Code153:14C0` | Code | `0xD13C0` | `0x15D2` | `0x1D10` |
| 154 (`0x9A`) | `Code154:14C8` | Code | `0xD2B20` | `0x974` | `0x1D10` |
| 155 (`0x9B`) | `Code155:14D0` | Code | `0xD35E0` | `0x584` | `0x1D10` |
| 156 (`0x9C`) | `Code156:14D8` | Code | `0xD3C00` | `0x162E` | `0x1D10` |
| 157 (`0x9D`) | `Code157:14E0` | Code | `0xD53A0` | `0x1A62` | `0x1D10` |
| 158 (`0x9E`) | `Code158:14E8` | Code | `0xD6FA0` | `0xCC6` | `0x1D10` |
| 159 (`0x9F`) | `Code159:14F0` | Code | `0xD7DE0` | `0x202` | `0x1D10` |
| 160 (`0xA0`) | `Code160:14F8` | Code | `0xD8080` | `0xF40` | `0x1D10` |
| 161 (`0xA1`) | `Code161:1500` | Code | `0xD9140` | `0x840` | `0x1D10` |
| 162 (`0xA2`) | `Code162:1508` | Code | `0xD9A20` | `0x41BC` | `0x1D10` |
| 163 (`0xA3`) | `Code163:1510` | Code | `0xDDFA0` | `0x139C` | `0x1D10` |
| 164 (`0xA4`) | `Code164:1518` | Code | `0xDF4A0` | `0x37E` | `0x1D10` |
| 165 (`0xA5`) | `Code165:1520` | Code | `0xDF8A0` | `0x41EE` | `0x1D10` |
| 166 (`0xA6`) | `Code166:1528` | Code | `0xE3D00` | `0x10BC` | `0x1D10` |
| 167 (`0xA7`) | `Code167:1530` | Code | `0xE4F40` | `0x181A` | `0x1D10` |
| 168 (`0xA8`) | `Code168:1538` | Code | `0xE68C0` | `0x766` | `0x1D10` |
| 169 (`0xA9`) | `Code169:1540` | Code | `0xE7100` | `0x540C` | `0x1D10` |
| 170 (`0xAA`) | `Code170:1548` | Code | `0xEC860` | `0x1552` | `0x1D10` |
| 171 (`0xAB`) | `Code171:1550` | Code | `0xEDFE0` | `0x2D68` | `0x1D10` |
| 172 (`0xAC`) | `Code172:1558` | Code | `0xF1020` | `0x24EA` | `0x1D10` |
| 173 (`0xAD`) | `Code173:1560` | Code | `0xF3680` | `0x2242` | `0x1D10` |
| 174 (`0xAE`) | `Code174:1568` | Code | `0xF5A80` | `0x14C6` | `0x1D10` |
| 175 (`0xAF`) | `Code175:1570` | Code | `0xF70C0` | `0xC0C` | `0x1D10` |
| 176 (`0xB0`) | `Code176:1578` | Code | `0xF7D60` | `0x1C6` | `0x1D10` |
| 177 (`0xB1`) | `Code177:1580` | Code | `0xF7F60` | `0x974` | `0x1D10` |
| 178 (`0xB2`) | `Code178:1588` | Code | `0xF8940` | `0x140` | `0x1D10` |
| 179 (`0xB3`) | `Code179:1590` | Code | `0xF8AA0` | `0x8D8` | `0x1D10` |
| 180 (`0xB4`) | `Code180:1598` | Code | `0xF93C0` | `0xE4` | `0x1C10` |
| 181 (`0xB5`) | `Code181:15A0` | Code | `0xF94C0` | `0x26A` | `0x1D10` |
| 182 (`0xB6`) | `Code182:15A8` | Code | `0xF97A0` | `0x1DA` | `0x1D10` |
| 183 (`0xB7`) | `Code183:15B0` | Code | `0xF99A0` | `0x227` | `0x1C10` |
| 184 (`0xB8`) | `Data184:15B8` | Data | `0xF9BE0` | `0x5940` | `0x0D51` |

## TB80BAS.DLL-4.html

Entry NE 2 at `1008:089E`. Auto data NE 199 at `1630`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x4760` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x5180` | `0x4B4B` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0xA5E0` | `0x5390` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0xFB80` | `0x1B50` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x117C0` | `0x1C4C` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x13640` | `0x44EA` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x17D00` | `0xD22` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x18AA0` | `0xC34` | `0x1D70` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x19740` | `0x1E02` | `0x1D70` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x1B5E0` | `0x2FF2` | `0x1D70` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x1E7A0` | `0x162` | `0x1D70` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x1E920` | `0x2C2C` | `0x1D70` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x216C0` | `0x1B1E` | `0x1D70` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x23260` | `0x1E3C` | `0x1D70` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x251E0` | `0x2806` | `0x1D70` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x27AA0` | `0x2BA4` | `0x1D70` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x2A720` | `0x226` | `0x1D70` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x2A960` | `0x2CD8` | `0x1D70` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x2D780` | `0x454` | `0x1D70` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x2DC20` | `0xF04` | `0x1D70` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x2EC40` | `0x7BE` | `0x1D70` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x2F4C0` | `0x644` | `0x1D70` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x2FB60` | `0x5B6E` | `0x1D70` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x35880` | `0xD70` | `0x1D70` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x36640` | `0xD6C` | `0x1D70` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x373E0` | `0x28E2` | `0x1D70` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x39E00` | `0x238E` | `0x1D70` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x3C240` | `0x1AAE` | `0x1D70` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x3DDC0` | `0x217C` | `0x1D70` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x3FFC0` | `0x34BE` | `0x1D70` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x435A0` | `0x289E` | `0x1D70` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x45F20` | `0xB24` | `0x1D70` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x46A80` | `0x275E` | `0x1D70` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x492A0` | `0x1CE` | `0x1D70` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x494A0` | `0xAE4` | `0x1D70` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x49FE0` | `0xAF0` | `0x1D70` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x4AB40` | `0x2D0` | `0x1D70` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x4AE40` | `0x222A` | `0x1D70` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x4D0E0` | `0x2BA8` | `0x1D70` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x4FDE0` | `0x1CA0` | `0x1D70` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x51B20` | `0x738` | `0x1D70` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x522A0` | `0x1156` | `0x1D70` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x53480` | `0x383` | `0x1D70` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0x53820` | `0x1194` | `0x1D70` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0x54A20` | `0x1094` | `0x1D70` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0x55B40` | `0x18BA` | `0x1D70` |
| 47 (`0x2F`) | `Code47:1170` | Code | `0x57460` | `0x4362` | `0x1D70` |
| 48 (`0x30`) | `Code48:1178` | Code | `0x5B940` | `0x1FC8` | `0x1D70` |
| 49 (`0x31`) | `Code49:1180` | Code | `0x5D9A0` | `0x4D6` | `0x1D70` |
| 50 (`0x32`) | `Code50:1188` | Code | `0x5DEC0` | `0xB42` | `0x1D70` |
| 51 (`0x33`) | `Code51:1190` | Code | `0x5EA40` | `0x3E8` | `0x1D70` |
| 52 (`0x34`) | `Code52:1198` | Code | `0x5EE80` | `0x57E` | `0x1D70` |
| 53 (`0x35`) | `Code53:11A0` | Code | `0x5F440` | `0xC7A` | `0x1D70` |
| 54 (`0x36`) | `Code54:11A8` | Code | `0x60100` | `0xEA6` | `0x1D70` |
| 55 (`0x37`) | `Code55:11B0` | Code | `0x61080` | `0xF7A` | `0x1D70` |
| 56 (`0x38`) | `Code56:11B8` | Code | `0x62020` | `0x1AE` | `0x1D70` |
| 57 (`0x39`) | `Code57:11C0` | Code | `0x621E0` | `0x1DB4` | `0x1D70` |
| 58 (`0x3A`) | `Code58:11C8` | Code | `0x64080` | `0x13CA` | `0x1D70` |
| 59 (`0x3B`) | `Code59:11D0` | Code | `0x65540` | `0x3C8` | `0x1D70` |
| 60 (`0x3C`) | `Code60:11D8` | Code | `0x65960` | `0x2D8E` | `0x1D70` |
| 61 (`0x3D`) | `Code61:11E0` | Code | `0x68780` | `0x27BC` | `0x1D70` |
| 62 (`0x3E`) | `Code62:11E8` | Code | `0x6B000` | `0x148E` | `0x1D70` |
| 63 (`0x3F`) | `Code63:11F0` | Code | `0x6C660` | `0x2C96` | `0x1D70` |
| 64 (`0x40`) | `Code64:11F8` | Code | `0x6F3A0` | `0x4C` | `0x1D70` |
| 65 (`0x41`) | `Code65:1200` | Code | `0x6F420` | `0xC52` | `0x1D70` |
| 66 (`0x42`) | `Code66:1208` | Code | `0x70120` | `0x1E24` | `0x1D70` |
| 67 (`0x43`) | `Code67:1210` | Code | `0x72000` | `0x606` | `0x1D70` |
| 68 (`0x44`) | `Code68:1218` | Code | `0x72660` | `0x480` | `0x1D70` |
| 69 (`0x45`) | `Code69:1220` | Code | `0x72B20` | `0x348C` | `0x1D70` |
| 70 (`0x46`) | `Code70:1228` | Code | `0x760E0` | `0x746` | `0x1D70` |
| 71 (`0x47`) | `Code71:1230` | Code | `0x768A0` | `0x5EE8` | `0x1D70` |
| 72 (`0x48`) | `Code72:1238` | Code | `0x7CA20` | `0x3B9E` | `0x1D70` |
| 73 (`0x49`) | `Code73:1240` | Code | `0x808C0` | `0x137E` | `0x1D70` |
| 74 (`0x4A`) | `Code74:1248` | Code | `0x81D00` | `0x38FA` | `0x1D70` |
| 75 (`0x4B`) | `Code75:1250` | Code | `0x85840` | `0x618` | `0x1D70` |
| 76 (`0x4C`) | `Code76:1258` | Code | `0x85EA0` | `0x11A0` | `0x1D70` |
| 77 (`0x4D`) | `Code77:1260` | Code | `0x87140` | `0xCAE` | `0x1D70` |
| 78 (`0x4E`) | `Code78:1268` | Code | `0x87EC0` | `0x2312` | `0x1D70` |
| 79 (`0x4F`) | `Code79:1270` | Code | `0x8A420` | `0x22` | `0x1D70` |
| 80 (`0x50`) | `Code80:1278` | Code | `0x8A460` | `0x7B56` | `0x1D70` |
| 81 (`0x51`) | `Code81:1280` | Code | `0x92220` | `0x4070` | `0x1D70` |
| 82 (`0x52`) | `Code82:1288` | Code | `0x96380` | `0xA2E` | `0x1D70` |
| 83 (`0x53`) | `Code83:1290` | Code | `0x96E80` | `0xF30` | `0x1D70` |
| 84 (`0x54`) | `Code84:1298` | Code | `0x97E60` | `0x422` | `0x1D70` |
| 85 (`0x55`) | `Code85:12A0` | Code | `0x98320` | `0x3C` | `0x0D60` |
| 86 (`0x56`) | `Code86:12A8` | Code | `0x98380` | `0x2C` | `0x1D30` |
| 87 (`0x57`) | `Code87:12B0` | Code | `0x983C0` | `0x68A` | `0x1D30` |
| 88 (`0x58`) | `Code88:12B8` | Code | `0x98AC0` | `0x179A` | `0x1D30` |
| 89 (`0x59`) | `Code89:12C0` | Code | `0x9A3A0` | `0x230` | `0x1D30` |
| 90 (`0x5A`) | `Code90:12C8` | Code | `0x9A600` | `0x1646` | `0x1D30` |
| 91 (`0x5B`) | `Code91:12D0` | Code | `0x9BD00` | `0x1C16` | `0x1D30` |
| 92 (`0x5C`) | `Code92:12D8` | Code | `0x9D9C0` | `0x2412` | `0x1D30` |
| 93 (`0x5D`) | `Code93:12E0` | Code | `0x9FFC0` | `0x2034` | `0x1D30` |
| 94 (`0x5E`) | `Code94:12E8` | Code | `0xA20A0` | `0x26DA` | `0x1D30` |
| 95 (`0x5F`) | `Code95:12F0` | Code | `0xA4880` | `0x654` | `0x1D30` |
| 96 (`0x60`) | `Code96:12F8` | Code | `0xA4F00` | `0x3F4` | `0x1D30` |
| 97 (`0x61`) | `Code97:1300` | Code | `0xA5320` | `0x4C2` | `0x1D30` |
| 98 (`0x62`) | `Code98:1308` | Code | `0xA5840` | `0x25B0` | `0x1D30` |
| 99 (`0x63`) | `Code99:1310` | Code | `0xA7EE0` | `0xD3A` | `0x1D30` |
| 100 (`0x64`) | `Code100:1318` | Code | `0xA8C60` | `0x948` | `0x1D30` |
| 101 (`0x65`) | `Code101:1320` | Code | `0xA95E0` | `0x4AA` | `0x1D30` |
| 102 (`0x66`) | `Code102:1328` | Code | `0xA9B00` | `0x12` | `0x1C30` |
| 103 (`0x67`) | `Code103:1330` | Code | `0xA9B20` | `0x60` | `0x1D30` |
| 104 (`0x68`) | `Code104:1338` | Code | `0xA9BC0` | `0x1026` | `0x1D30` |
| 105 (`0x69`) | `Code105:1340` | Code | `0xAAC60` | `0x25DC` | `0x1D30` |
| 106 (`0x6A`) | `Code106:1348` | Code | `0xAD2A0` | `0xF06` | `0x1D30` |
| 107 (`0x6B`) | `Code107:1350` | Code | `0xAE2A0` | `0x642A` | `0x1D30` |
| 108 (`0x6C`) | `Code108:1358` | Code | `0xB4860` | `0x1974` | `0x1D30` |
| 109 (`0x6D`) | `Code109:1360` | Code | `0xB6280` | `0xD86` | `0x1D30` |
| 110 (`0x6E`) | `Code110:1368` | Code | `0xB7080` | `0x15B4` | `0x1D30` |
| 111 (`0x6F`) | `Code111:1370` | Code | `0xB86E0` | `0x134E` | `0x1D30` |
| 112 (`0x70`) | `Code112:1378` | Code | `0xB9D80` | `0x4D4` | `0x1D30` |
| 113 (`0x71`) | `Code113:1380` | Code | `0xBA280` | `0x186` | `0x1D30` |
| 114 (`0x72`) | `Code114:1388` | Code | `0xBA440` | `0x6A` | `0x1C30` |
| 115 (`0x73`) | `Code115:1390` | Code | `0xBA4C0` | `0xC0C` | `0x1D30` |
| 116 (`0x74`) | `Code116:1398` | Code | `0xBB120` | `0x3D50` | `0x1D30` |
| 117 (`0x75`) | `Code117:13A0` | Code | `0xBF040` | `0xDCE` | `0x1D30` |
| 118 (`0x76`) | `Code118:13A8` | Code | `0xBFE40` | `0x63A` | `0x1D30` |
| 119 (`0x77`) | `Code119:13B0` | Code | `0xC0520` | `0x2D1C` | `0x1D30` |
| 120 (`0x78`) | `Code120:13B8` | Code | `0xC3440` | `0x1EA8` | `0x1D30` |
| 121 (`0x79`) | `Code121:13C0` | Code | `0xC53E0` | `0x7DE` | `0x1D30` |
| 122 (`0x7A`) | `Code122:13C8` | Code | `0xC5C60` | `0xC86` | `0x1D30` |
| 123 (`0x7B`) | `Code123:13D0` | Code | `0xC6B00` | `0x96E` | `0x1D30` |
| 124 (`0x7C`) | `Code124:13D8` | Code | `0xC74E0` | `0x1D2` | `0x1D30` |
| 125 (`0x7D`) | `Code125:13E0` | Code | `0xC76E0` | `0x322` | `0x1D30` |
| 126 (`0x7E`) | `Code126:13E8` | Code | `0xC7A40` | `0x35C` | `0x1D30` |
| 127 (`0x7F`) | `Code127:13F0` | Code | `0xC7DE0` | `0x3246` | `0x1D30` |
| 128 (`0x80`) | `Code128:13F8` | Code | `0xCB1E0` | `0x654` | `0x1D30` |
| 129 (`0x81`) | `Code129:1400` | Code | `0xCB8A0` | `0x1744` | `0x1D30` |
| 130 (`0x82`) | `Code130:1408` | Code | `0xCD0C0` | `0x540` | `0x1D30` |
| 131 (`0x83`) | `Code131:1410` | Code | `0xCD680` | `0x1D2` | `0x1D30` |
| 132 (`0x84`) | `Code132:1418` | Code | `0xCD880` | `0xF30` | `0x1D30` |
| 133 (`0x85`) | `Code133:1420` | Code | `0xCE840` | `0x120E` | `0x1D30` |
| 134 (`0x86`) | `Code134:1428` | Code | `0xCFB60` | `0xF3C` | `0x1D30` |
| 135 (`0x87`) | `Code135:1430` | Code | `0xD0B20` | `0xD9C` | `0x1D30` |
| 136 (`0x88`) | `Code136:1438` | Code | `0xD1940` | `0xAF4` | `0x1D30` |
| 137 (`0x89`) | `Code137:1440` | Code | `0xD2500` | `0xD9A` | `0x1D30` |
| 138 (`0x8A`) | `Code138:1448` | Code | `0xD3340` | `0x11B6` | `0x1D30` |
| 139 (`0x8B`) | `Code139:1450` | Code | `0xD45A0` | `0xA7E` | `0x1D30` |
| 140 (`0x8C`) | `Code140:1458` | Code | `0xD50A0` | `0xAB6` | `0x1D30` |
| 141 (`0x8D`) | `Code141:1460` | Code | `0xD5C40` | `0x12C6` | `0x1D30` |
| 142 (`0x8E`) | `Code142:1468` | Code | `0xD6F80` | `0xC60` | `0x1D30` |
| 143 (`0x8F`) | `Code143:1470` | Code | `0xD7CA0` | `0x169A` | `0x1D30` |
| 144 (`0x90`) | `Code144:1478` | Code | `0xD93E0` | `0xBC6` | `0x1D30` |
| 145 (`0x91`) | `Code145:1480` | Code | `0xDA000` | `0x15E` | `0x1D30` |
| 146 (`0x92`) | `Code146:1488` | Code | `0xDA180` | `0x652` | `0x1D30` |
| 147 (`0x93`) | `Code147:1490` | Code | `0xDA860` | `0x1322` | `0x1D30` |
| 148 (`0x94`) | `Code148:1498` | Code | `0xDBC20` | `0xCC8` | `0x1D30` |
| 149 (`0x95`) | `Code149:14A0` | Code | `0xDC980` | `0x82E` | `0x1D30` |
| 150 (`0x96`) | `Code150:14A8` | Code | `0xDD240` | `0xD2A` | `0x1D30` |
| 151 (`0x97`) | `Code151:14B0` | Code | `0xDDFE0` | `0x307C` | `0x1D30` |
| 152 (`0x98`) | `Code152:14B8` | Code | `0xE1240` | `0x1156` | `0x1D30` |
| 153 (`0x99`) | `Code153:14C0` | Code | `0xE2440` | `0x13FE` | `0x1D30` |
| 154 (`0x9A`) | `Code154:14C8` | Code | `0xE3A00` | `0x1C5C` | `0x1D30` |
| 155 (`0x9B`) | `Code155:14D0` | Code | `0xE5700` | `0x1924` | `0x1D30` |
| 156 (`0x9C`) | `Code156:14D8` | Code | `0xE70C0` | `0x754` | `0x1D30` |
| 157 (`0x9D`) | `Code157:14E0` | Code | `0xE7840` | `0x1638` | `0x1D30` |
| 158 (`0x9E`) | `Code158:14E8` | Code | `0xE9000` | `0x17DC` | `0x1D30` |
| 159 (`0x9F`) | `Code159:14F0` | Code | `0xEA920` | `0x1F34` | `0x1D30` |
| 160 (`0xA0`) | `Code160:14F8` | Code | `0xEC9A0` | `0x10EE` | `0x1D30` |
| 161 (`0xA1`) | `Code161:1500` | Code | `0xEDBC0` | `0xAE4` | `0x1D30` |
| 162 (`0xA2`) | `Code162:1508` | Code | `0xEE700` | `0x49B8` | `0x1D30` |
| 163 (`0xA3`) | `Code163:1510` | Code | `0xF3160` | `0x8C` | `0x1D30` |
| 164 (`0xA4`) | `Code164:1518` | Code | `0xF3200` | `0x19C` | `0x1D30` |
| 165 (`0xA5`) | `Code165:1520` | Code | `0xF33C0` | `0x1B8E` | `0x1D30` |
| 166 (`0xA6`) | `Code166:1528` | Code | `0xF5080` | `0x4D2` | `0x1D30` |
| 167 (`0xA7`) | `Code167:1530` | Code | `0xF5580` | `0xBF6` | `0x1D30` |
| 168 (`0xA8`) | `Code168:1538` | Code | `0xF61C0` | `0x4BA` | `0x1D30` |
| 169 (`0xA9`) | `Code169:1540` | Code | `0xF66C0` | `0x90E` | `0x1D30` |
| 170 (`0xAA`) | `Code170:1548` | Code | `0xF7020` | `0x30C` | `0x1D30` |
| 171 (`0xAB`) | `Code171:1550` | Code | `0xF7360` | `0x2A8` | `0x1D30` |
| 172 (`0xAC`) | `Code172:1558` | Code | `0xF7660` | `0x1EA` | `0x1D30` |
| 173 (`0xAD`) | `Code173:1560` | Code | `0xF7880` | `0x30E` | `0x1D30` |
| 174 (`0xAE`) | `Code174:1568` | Code | `0xF7BC0` | `0x5C4` | `0x1D30` |
| 175 (`0xAF`) | `Code175:1570` | Code | `0xF81E0` | `0x1D04` | `0x1D30` |
| 176 (`0xB0`) | `Code176:1578` | Code | `0xF9FA0` | `0x3512` | `0x1D30` |
| 177 (`0xB1`) | `Code177:1580` | Code | `0xFD5A0` | `0x754` | `0x1D30` |
| 178 (`0xB2`) | `Code178:1588` | Code | `0xFDD80` | `0x300` | `0x1D30` |
| 179 (`0xB3`) | `Code179:1590` | Code | `0xFE0E0` | `0x532` | `0x1D30` |
| 180 (`0xB4`) | `Code180:1598` | Code | `0xFE660` | `0x1180` | `0x1D30` |
| 181 (`0xB5`) | `Code181:15A0` | Code | `0xFF820` | `0x8D8` | `0x1D30` |
| 182 (`0xB6`) | `Code182:15A8` | Code | `0x100140` | `0x610` | `0x1D30` |
| 183 (`0xB7`) | `Code183:15B0` | Code | `0x100780` | `0x163A` | `0x1D30` |
| 184 (`0xB8`) | `Code184:15B8` | Code | `0x101E40` | `0x16C` | `0x1D30` |
| 185 (`0xB9`) | `Code185:15C0` | Code | `0x101FC0` | `0x140` | `0x1D30` |
| 186 (`0xBA`) | `Code186:15C8` | Code | `0x102120` | `0xEE6` | `0x1D30` |
| 187 (`0xBB`) | `Code187:15D0` | Code | `0x103060` | `0x956` | `0x1D30` |
| 188 (`0xBC`) | `Code188:15D8` | Code | `0x1039E0` | `0x86` | `0x1D30` |
| 189 (`0xBD`) | `Code189:15E0` | Code | `0x103A80` | `0x59CC` | `0x1D30` |
| 190 (`0xBE`) | `Code190:15E8` | Code | `0x109620` | `0x23A` | `0x1D30` |
| 191 (`0xBF`) | `Code191:15F0` | Code | `0x1098A0` | `0xE2` | `0x1D30` |
| 192 (`0xC0`) | `Code192:15F8` | Code | `0x1099A0` | `0xE2E` | `0x1D30` |
| 193 (`0xC1`) | `Data193:1600` | Data | `0x10A800` | `0x2A0` | `0x0C71` |
| 194 (`0xC2`) | `Data194:1608` | Data | `0x10AAA0` | `0x55C` | `0x0D71` |
| 195 (`0xC3`) | `Data195:1610` | Data | `0x10B040` | `0x3F0` | `0x0C71` |
| 196 (`0xC4`) | `Data196:1618` | Data | `0x10B440` | `0x1E` | `0x0C71` |
| 197 (`0xC5`) | `Data197:1620` | Data | `0x10B460` | `0x1A72` | `0x0C71` |
| 198 (`0xC6`) | `Data198:1628` | Data | `0x10CEE0` | `0x80` | `0x0C71` |
| 199 (`0xC7`) | `Data199:1630` | Data | `0x10CF60` | `0x3BB8` | `0x0D71` |

## TB80BMP.DLL.html

Entry NE 2 at `1008:02D8`. Auto data NE 27 at `10D0`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xB20` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1540` | `0x3343` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x4EE0` | `0x220A` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x72A0` | `0x32A` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x7620` | `0x1E6` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x7860` | `0x54` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x78E0` | `0xAC0` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x84C0` | `0x40C` | `0x1D70` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x88E0` | `0x1BE` | `0x1D70` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x8B00` | `0x8DAA` | `0x1D70` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x11F20` | `0x3C` | `0x0D60` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x11F80` | `0xB0` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x12060` | `0x3E4` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x12480` | `0x65A` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x12B80` | `0x126A` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x13F20` | `0x136C` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x153A0` | `0x996` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x15DE0` | `0x946` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x168A0` | `0xB76` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x174A0` | `0xBBC` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x18100` | `0x1A8A` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x19C20` | `0x3CC` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x1A020` | `0x1C4` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x1A240` | `0x2E1` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x1A580` | `0x43B` | `0x1D30` |
| 26 (`0x1A`) | `Data26:10C8` | Data | `0x1AB20` | `0x6` | `0x0C71` |
| 27 (`0x1B`) | `Data27:10D0` | Data | `0x1AB40` | `0x23AE` | `0x0D71` |

## TB80CMP.ghidra.dll.html

Entry NE 2 at `1008:00BE`. Auto data NE 47 at `1170`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x520` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xF40` | `0x224D` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x3360` | `0x1CC4` | `0x1D50` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x51E0` | `0x3C` | `0x0D40` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x5240` | `0x12` | `0x1C10` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x5260` | `0x8EB6` | `0x1D10` |
| 7 (`0x07`) | `Code7:1030` | Code | `0xE180` | `0xED8` | `0x1D10` |
| 8 (`0x08`) | `Code8:1038` | Code | `0xF0A0` | `0x1166` | `0x1D10` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x10280` | `0x10D0` | `0x1D10` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x113C0` | `0x1F4A` | `0x1D10` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x13360` | `0xF0E` | `0x1D10` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x142A0` | `0x632` | `0x1D10` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x14940` | `0x2AE` | `0x1D10` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x14C20` | `0xAC0` | `0x1D10` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x15740` | `0x15BC` | `0x1D10` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x16D80` | `0x2320` | `0x1D10` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x19140` | `0x1AAE` | `0x1D10` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x1AC80` | `0x25FA` | `0x1D10` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x1D360` | `0x42E` | `0x1D10` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x1D7C0` | `0x1490` | `0x1D10` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x1ECA0` | `0x1EE6` | `0x1D10` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x20BE0` | `0x263A` | `0x1D10` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x232A0` | `0x312C` | `0x1D10` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x26460` | `0x23DA` | `0x1D10` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x28880` | `0x150C` | `0x1D10` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x29DE0` | `0xF60` | `0x1D10` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x2ADA0` | `0x95E` | `0x1D10` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x2B740` | `0x1822` | `0x1D10` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x2CFA0` | `0x1CF0` | `0x1D10` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x2ECE0` | `0x138C` | `0x1D10` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x300A0` | `0x4FAC` | `0x1D10` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x35080` | `0x7BC` | `0x1D10` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x35880` | `0x22` | `0x1C10` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x358C0` | `0x249C` | `0x1D10` |
| 35 (`0x23`) | `Data35:1110` | Data | `0x37E20` | `0x9CFE` | `0x0CF1` |
| 36 (`0x24`) | `Data36:1118` | Data | `0x41B20` | `0x14` | `0x0C71` |
| 37 (`0x25`) | `Data37:1120` | Data | `0x41B40` | `0x28` | `0x0C71` |
| 38 (`0x26`) | `Data38:1128` | Data | `0x41B80` | `0xF0` | `0x0C71` |
| 39 (`0x27`) | `Data39:1130` | Data | `0x41C80` | `0xA` | `0x0C71` |
| 40 (`0x28`) | `Data40:1138` | Data | `0x41CA0` | `0x4D4` | `0x0C71` |
| 41 (`0x29`) | `Data41:1140` | Data | `0x42180` | `0x508` | `0x0C71` |
| 42 (`0x2A`) | `Data42:1148` | Data | `0x426A0` | `0x6A0` | `0x0C71` |
| 43 (`0x2B`) | `Data43:1150` | Data | `0x42D40` | `0xC40` | `0x0C71` |
| 44 (`0x2C`) | `Data44:1158` | Data | `0x43980` | `0x8C0` | `0x0C71` |
| 45 (`0x2D`) | `Data45:1160` | Data | `0x44240` | `0x1F3F` | `0x0C71` |
| 46 (`0x2E`) | `Data46:1168` | Data | `0x46180` | `0x2` | `0x0C71` |
| 47 (`0x2F`) | `Data47:1170` | Data | `0x461A0` | `0x74C8` | `0x0D71` |

## TB80ENU1.DLL.html

Entry NE 6 at `1028:0054`. Auto data NE 8 at `1038`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x8C0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x12E0` | `0x42` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x1340` | `0x24` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x1380` | `0x84` | `0x1C70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x1420` | `0x2C` | `0x1C70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x1460` | `0x74D` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x1C40` | `0x54` | `0x1D70` |
| 8 (`0x08`) | `Data8:1038` | Data | `0x1CC0` | `0x172` | `0x0C71` |

## TB80FLT.DLL.html

Entry NE 23 at `10B0:0484`. Auto data NE 28 at `10D8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xC40` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1660` | `0x3C` | `0x0D60` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x16C0` | `0x2F86` | `0x1D30` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x4800` | `0xF02` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x57C0` | `0x40` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x5840` | `0x2F64` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x8A40` | `0x746C` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x102A0` | `0x19C` | `0x1D30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x10480` | `0x17B2` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x11E20` | `0x2734` | `0x1D30` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x14740` | `0xF1E` | `0x1D30` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x157C0` | `0xF18` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x16880` | `0x1B66` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x184E0` | `0xC16` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x191C0` | `0x31A` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x19540` | `0x1D0A` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x1B2E0` | `0x890` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x1BBC0` | `0x6C4` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x1C360` | `0x1180` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x1D520` | `0x64` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x1D5C0` | `0xE6` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x1D6C0` | `0xC0E` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x1E360` | `0x24C5` | `0x1D70` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x20A60` | `0x8D8` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x21380` | `0x140` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x214E0` | `0x21F` | `0x1D30` |
| 27 (`0x1B`) | `Data27:10D0` | Data | `0x21740` | `0x90` | `0x0C71` |
| 28 (`0x1C`) | `Data28:10D8` | Data | `0x217E0` | `0x3218` | `0x0D71` |

## TB80JPG.DLL.html

Entry NE 2 at `1008:A5C2`. Auto data NE 3 at `1010`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x250` | `0x3B` | `0x0D60` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x2A0` | `0xDB9C` | `0x1D70` |
| 3 (`0x03`) | `Data3:1010` | Data | `0xE8A0` | `0xEA5` | `0x0D71` |

## TB80LNL.DLL.html

Entry NE 15 at `1070:0054`. Auto data NE 39 at `1130`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xBC0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x15E0` | `0x21A` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x1840` | `0x454` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x1E20` | `0x5EC` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x2480` | `0x906` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x2DE0` | `0x52E` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x3340` | `0x160E` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x4A80` | `0x90E` | `0x1D70` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x5440` | `0x4C26` | `0x1D70` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0xA1C0` | `0x2004` | `0x1D70` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0xC280` | `0xEA2` | `0x1D70` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0xD280` | `0x1E3A` | `0x1D70` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0xF0E0` | `0x32B6` | `0x1D70` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x12460` | `0x3C` | `0x0D60` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x124C0` | `0x2181` | `0x1D70` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x14840` | `0x40` | `0x1C30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x14880` | `0x136` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x149E0` | `0x204` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x14C00` | `0x1648` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x16300` | `0x68A` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x169E0` | `0x3780` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x1A280` | `0x3AC8` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x1DE20` | `0xF34` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x1EEA0` | `0xABE` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x1FA00` | `0x392` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x1FDE0` | `0x45F2` | `0x1D30` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x244A0` | `0x858` | `0x1D30` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x24D60` | `0x1A08` | `0x1D30` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x26840` | `0x818` | `0x1D30` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x270C0` | `0xA16` | `0x1D30` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x27B40` | `0xDF6` | `0x1D30` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x289A0` | `0x1E26` | `0x1D30` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x2A880` | `0xF8C` | `0x1D30` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x2B8A0` | `0x8D8` | `0x1D30` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x2C1C0` | `0xE2` | `0x1D30` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x2C2E0` | `0x140` | `0x1D30` |
| 37 (`0x25`) | `Data37:1120` | Data | `0x2C440` | `0x10` | `0x0C71` |
| 38 (`0x26`) | `Data38:1128` | Data | `0x2C460` | `0x10` | `0x0C71` |
| 39 (`0x27`) | `Data39:1130` | Data | `0x2C480` | `0x31B8` | `0x0D71` |

## TB80MM.DLL.html

Entry NE 3 at `1010:0054`. Auto data NE 22 at `10A8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x480` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xEA0` | `0x26` | `0x0D60` |
| 3 (`0x03`) | `Code3:1010` | Code | `0xEE0` | `0xC63` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x1C00` | `0x3CA` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x2060` | `0x5E2` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x26A0` | `0xBC` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x2780` | `0x1838` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x4080` | `0x8C8` | `0x1D70` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x49A0` | `0x40C` | `0x1D70` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x4DC0` | `0x1BE` | `0x1D70` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x4FE0` | `0x210` | `0x1D70` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x5220` | `0x3C` | `0x0D60` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x5280` | `0xA3E` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x5D20` | `0x70A` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x6460` | `0x53E` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x6A20` | `0x464` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x6F00` | `0x142` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x7080` | `0xB4A` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x7C80` | `0x446` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x8120` | `0xC9A` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x8F00` | `0x1C4` | `0x1D30` |
| 22 (`0x16`) | `Data22:10A8` | Data | `0x9120` | `0x13D2` | `0x0D71` |

## TB80NET.EXE.html

Entry NE 2 at `1008:0120`. Auto data NE 45 at `1160`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x3A0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xDC0` | `0x17F4` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x2660` | `0x16A8` | `0x1D10` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x3F00` | `0x206` | `0x1D10` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x4140` | `0x1904` | `0x1D10` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x5B20` | `0xBA4` | `0x1D10` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x6700` | `0x7A` | `0x1D10` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x67A0` | `0xBEC` | `0x1D10` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x7400` | `0x930` | `0x1D10` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x7DC0` | `0x8D8` | `0x1D10` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x86E0` | `0x1BA` | `0x1D10` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x8900` | `0x974` | `0x1D10` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x92E0` | `0xB60` | `0x1D10` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x9EA0` | `0x3F0` | `0x1D10` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0xA2C0` | `0xE4` | `0x1D10` |
| 16 (`0x10`) | `Code16:1078` | Code | `0xA3E0` | `0x140` | `0x1D10` |
| 17 (`0x11`) | `Code17:1080` | Code | `0xA540` | `0x26A` | `0x1D10` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xA820` | `0x1DA` | `0x1D10` |
| 19 (`0x13`) | `Code19:1090` | Code | `0xAA20` | `0x698` | `0x1D10` |
| 20 (`0x14`) | `Code20:1098` | Code | `0xB100` | `0x1C6` | `0x1D10` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0xB300` | `0x1040` | `0x1D10` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0xC3A0` | `0x9A4` | `0x1D10` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xCD80` | `0x9A` | `0x1D10` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xCE40` | `0xA28` | `0x1D10` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0xD8A0` | `0x1CA4` | `0x1D10` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0xF560` | `0x9D6` | `0x1D10` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0xFF60` | `0x64` | `0x1D10` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0xFFE0` | `0x1D6E` | `0x1D10` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x11D60` | `0x25A` | `0x1D10` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x11FE0` | `0xDEC` | `0x1D10` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x12E00` | `0x1CE` | `0x1C10` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x12FE0` | `0x6AA` | `0x1C10` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x136A0` | `0x918` | `0x1D10` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x13FE0` | `0x50A` | `0x1D10` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x14500` | `0x162` | `0x1D10` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x146C0` | `0x1E4C` | `0x1D10` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x16640` | `0x772` | `0x1D10` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x16DE0` | `0xEBD` | `0x1D10` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x17D00` | `0x45A` | `0x1D10` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x18200` | `0x80A` | `0x1D10` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x18A40` | `0xB9E` | `0x1D10` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x196E0` | `0x1F1` | `0x1D10` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x19920` | `0x662` | `0x1D10` |
| 44 (`0x2C`) | `Data44:1158` | Data | `0x1A020` | `0xE` | `0x0C71` |
| 45 (`0x2D`) | `Data45:1160` | Data | `0x1A040` | `0x2DB0` | `0x0D71` |

## TB80OCX.DLL.html

Entry NE 1 at `1000:0054`. Auto data NE 53 at `11A0`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x3360` | `0x2AC5` | `0x1D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x8420` | `0x6A7` | `0x1D10` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x8B60` | `0x10CC` | `0x1D10` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x9D00` | `0x536F` | `0x1D10` |
| 5 (`0x05`) | `Code5:1020` | Code | `0xF2A0` | `0x336` | `0x1D10` |
| 6 (`0x06`) | `Code6:1028` | Code | `0xF600` | `0x2CC` | `0x1D10` |
| 7 (`0x07`) | `Code7:1030` | Code | `0xF900` | `0x8E3` | `0x1D10` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x10240` | `0x882` | `0x1D10` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x10B20` | `0x1D9C` | `0x1D10` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x129E0` | `0x370` | `0x1D10` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x12DA0` | `0x2511` | `0x1D10` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x153E0` | `0x947` | `0x1D10` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x15D80` | `0x231` | `0x1D10` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x15FE0` | `0x5A6` | `0x1D10` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x16600` | `0x1B67` | `0x1D10` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x182C0` | `0x21AE` | `0x1D10` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x1A5A0` | `0x121E` | `0x1D10` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x1B8A0` | `0x133D` | `0x1D10` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x1CC80` | `0x1C26` | `0x1D10` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x1E980` | `0x1112` | `0x1D10` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x1FB20` | `0x755` | `0x1D10` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x202C0` | `0x720` | `0x1D10` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x20A40` | `0x1078` | `0x1D10` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x21B60` | `0x9E0` | `0x1D10` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x225A0` | `0x11F8` | `0x1D10` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x23880` | `0x760` | `0x1D10` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x24040` | `0x7BE` | `0x1D10` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x24880` | `0x15A` | `0x1D10` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x24A00` | `0x7C7` | `0x1D10` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x25240` | `0x444` | `0x1D10` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x256C0` | `0x3CE` | `0x1D10` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x25AC0` | `0x2DA` | `0x1D10` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x25DE0` | `0x25C` | `0x1D10` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x26060` | `0x2E3` | `0x1D10` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x26360` | `0x4714` | `0x1D10` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x2AC00` | `0xE0` | `0x1D10` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x2AD00` | `0xCC6` | `0x1D10` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x2B9E0` | `0x2055` | `0x1D10` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x2DA80` | `0x41C` | `0x1D10` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x2DF00` | `0x14E` | `0x1D10` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x2E060` | `0x21F` | `0x1D10` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x2E2C0` | `0x6C3` | `0x1D10` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x2EA60` | `0x117F` | `0x1D10` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0x2FC20` | `0x14DA` | `0x1D10` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0x31120` | `0x53` | `0x1D10` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0x311A0` | `0xD4A` | `0x1D10` |
| 47 (`0x2F`) | `Data47:1170` | Data | `0x6060` | `0x20` | `0x0C71` |
| 48 (`0x30`) | `Data48:1178` | Data | `0x60A0` | `0x9C` | `0x0D71` |
| 49 (`0x31`) | `Data49:1180` | Data | `0x6160` | `0x20` | `0x0C71` |
| 50 (`0x32`) | `Data50:1188` | Data | `0x0` | `0x0` | `0x0C71` |
| 51 (`0x33`) | `Data51:1190` | Data | `0x0` | `0x0` | `0x0C71` |
| 52 (`0x34`) | `Data52:1198` | Data | `0x61A0` | `0x90` | `0x0C71` |
| 53 (`0x35`) | `Data53:11A0` | Data | `0x6240` | `0x2148` | `0x0D71` |

## TB80RCR.DLL.html

Entry NE 2 at `1008:A998`. Auto data NE 5 at `1020`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xCC0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x16D0` | `0xD7F7` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0xF9E0` | `0xCD02` | `0x1D50` |
| 4 (`0x04`) | `Data4:1018` | Data | `0x1CE70` | `0x6` | `0x0C71` |
| 5 (`0x05`) | `Data5:1020` | Data | `0x1CE80` | `0x1C17` | `0x0D71` |

## TB80RTM.EXE-5.html

Entry NE 2 at `1008:035A`. Auto data NE 139 at `1450`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x1420` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1E40` | `0x4A7C` | `0x0D40` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x7240` | `0x1AFA` | `0x1D50` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x8EE0` | `0x276E` | `0x1D50` |
| 5 (`0x05`) | `Code5:1020` | Code | `0xB860` | `0x2ACC` | `0x1D50` |
| 6 (`0x06`) | `Code6:1028` | Code | `0xE540` | `0x55E` | `0x1D50` |
| 7 (`0x07`) | `Code7:1030` | Code | `0xEAC0` | `0x41A` | `0x1D50` |
| 8 (`0x08`) | `Code8:1038` | Code | `0xEF80` | `0x38A` | `0x1D50` |
| 9 (`0x09`) | `Code9:1040` | Code | `0xF3C0` | `0x9D0` | `0x1D50` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0xFE60` | `0x6AA` | `0x1D50` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x10640` | `0x1A7C` | `0x1D50` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x121E0` | `0xAD2` | `0x1D50` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x12E40` | `0x16AA` | `0x1D50` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x147C0` | `0x430` | `0x1D50` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x14CA0` | `0x1D44` | `0x1D50` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x16C80` | `0x1510` | `0x1D50` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x18320` | `0x9E6` | `0x1D50` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x18E00` | `0x3B8` | `0x1D50` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x19220` | `0x638` | `0x1D50` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x19900` | `0x2C9A` | `0x1D50` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x1C920` | `0x1066` | `0x1D50` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x1DA80` | `0x22B8` | `0x1D50` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x20040` | `0x3314` | `0x1D50` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x234E0` | `0x351A` | `0x1D50` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x26CE0` | `0x3612` | `0x1D50` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x2A6A0` | `0x1E18` | `0x1D50` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x2C5C0` | `0x3320` | `0x1D50` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x2FB40` | `0x44C` | `0x1D50` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x30060` | `0xEAA` | `0x1D50` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x310A0` | `0x153C` | `0x1D50` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x32780` | `0x2090` | `0x1D50` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x34B40` | `0x43CE` | `0x1D50` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x39160` | `0x994` | `0x1D50` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x39BE0` | `0x994` | `0x1D50` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x3A620` | `0x58C0` | `0x1D50` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x40120` | `0x3DE` | `0x1D50` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x40560` | `0x127A` | `0x1D50` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x41980` | `0xA6C` | `0x1D50` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x424C0` | `0x40E2` | `0x1D50` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x467A0` | `0xB5A` | `0x1D50` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x473C0` | `0x2C` | `0x1C50` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x47400` | `0xDD8` | `0x1D50` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x48360` | `0x50A` | `0x1D50` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0x488E0` | `0x5EC` | `0x1D50` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0x48F00` | `0x84` | `0x1D50` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0x48FA0` | `0x854` | `0x1D50` |
| 47 (`0x2F`) | `Code47:1170` | Code | `0x49920` | `0xC76` | `0x1D50` |
| 48 (`0x30`) | `Code48:1178` | Code | `0x4A680` | `0x1022` | `0x1D10` |
| 49 (`0x31`) | `Code49:1180` | Code | `0x4B7A0` | `0x1D00` | `0x1D10` |
| 50 (`0x32`) | `Code50:1188` | Code | `0x4D6A0` | `0x35B6` | `0x1D10` |
| 51 (`0x33`) | `Code51:1190` | Code | `0x50F80` | `0x1914` | `0x1D10` |
| 52 (`0x34`) | `Code52:1198` | Code | `0x52AE0` | `0x204` | `0x1D10` |
| 53 (`0x35`) | `Code53:11A0` | Code | `0x52D40` | `0x81A` | `0x1D10` |
| 54 (`0x36`) | `Code54:11A8` | Code | `0x53620` | `0x16A` | `0x1D10` |
| 55 (`0x37`) | `Code55:11B0` | Code | `0x537E0` | `0x50A` | `0x1D10` |
| 56 (`0x38`) | `Code56:11B8` | Code | `0x53DC0` | `0xD54` | `0x1D10` |
| 57 (`0x39`) | `Code57:11C0` | Code | `0x54C40` | `0x9F2` | `0x1D10` |
| 58 (`0x3A`) | `Code58:11C8` | Code | `0x556E0` | `0x22` | `0x1D10` |
| 59 (`0x3B`) | `Code59:11D0` | Code | `0x55720` | `0x106` | `0x1D10` |
| 60 (`0x3C`) | `Code60:11D8` | Code | `0x55840` | `0xD72` | `0x1D10` |
| 61 (`0x3D`) | `Code61:11E0` | Code | `0x56680` | `0x14` | `0x1C10` |
| 62 (`0x3E`) | `Code62:11E8` | Code | `0x566A0` | `0xD72` | `0x1D10` |
| 63 (`0x3F`) | `Code63:11F0` | Code | `0x57560` | `0x4C` | `0x1D10` |
| 64 (`0x40`) | `Code64:11F8` | Code | `0x575C0` | `0x1B0` | `0x1D10` |
| 65 (`0x41`) | `Code65:1200` | Code | `0x577A0` | `0x496` | `0x1D10` |
| 66 (`0x42`) | `Code66:1208` | Code | `0x57C80` | `0xA82` | `0x1D10` |
| 67 (`0x43`) | `Code67:1210` | Code | `0x587A0` | `0xC7E` | `0x1D10` |
| 68 (`0x44`) | `Code68:1218` | Code | `0x59580` | `0x34B8` | `0x1D10` |
| 69 (`0x45`) | `Code69:1220` | Code | `0x5CD60` | `0x8A74` | `0x1D10` |
| 70 (`0x46`) | `Code70:1228` | Code | `0x65D20` | `0x2080` | `0x1D10` |
| 71 (`0x47`) | `Code71:1230` | Code | `0x67FC0` | `0xCF4` | `0x1D10` |
| 72 (`0x48`) | `Code72:1238` | Code | `0x68DA0` | `0x32E` | `0x1D10` |
| 73 (`0x49`) | `Code73:1240` | Code | `0x69140` | `0x17F0` | `0x1D10` |
| 74 (`0x4A`) | `Code74:1248` | Code | `0x6A9E0` | `0x1890` | `0x1D10` |
| 75 (`0x4B`) | `Code75:1250` | Code | `0x6C3C0` | `0xA80` | `0x1D10` |
| 76 (`0x4C`) | `Code76:1258` | Code | `0x6CF20` | `0xBE2` | `0x1D10` |
| 77 (`0x4D`) | `Code77:1260` | Code | `0x6DB80` | `0x31FC` | `0x1D10` |
| 78 (`0x4E`) | `Code78:1268` | Code | `0x70FC0` | `0x1742` | `0x1D10` |
| 79 (`0x4F`) | `Code79:1270` | Code | `0x72880` | `0x138` | `0x1D10` |
| 80 (`0x50`) | `Code80:1278` | Code | `0x72A00` | `0x14E` | `0x1D10` |
| 81 (`0x51`) | `Code81:1280` | Code | `0x72BA0` | `0x57E` | `0x1D10` |
| 82 (`0x52`) | `Code82:1288` | Code | `0x73160` | `0x784` | `0x1D10` |
| 83 (`0x53`) | `Code83:1290` | Code | `0x73920` | `0xD9E` | `0x1D10` |
| 84 (`0x54`) | `Code84:1298` | Code | `0x747C0` | `0xC4C` | `0x1D10` |
| 85 (`0x55`) | `Code85:12A0` | Code | `0x754E0` | `0x96E` | `0x1D10` |
| 86 (`0x56`) | `Code86:12A8` | Code | `0x75F00` | `0x22F6` | `0x1D10` |
| 87 (`0x57`) | `Code87:12B0` | Code | `0x78920` | `0xDAA` | `0x1D10` |
| 88 (`0x58`) | `Code88:12B8` | Code | `0x797A0` | `0x258` | `0x1D10` |
| 89 (`0x59`) | `Code89:12C0` | Code | `0x79A40` | `0x1EF0` | `0x1D10` |
| 90 (`0x5A`) | `Code90:12C8` | Code | `0x7BB40` | `0xAE` | `0x1D10` |
| 91 (`0x5B`) | `Code91:12D0` | Code | `0x7BC00` | `0x7B6` | `0x1D10` |
| 92 (`0x5C`) | `Code92:12D8` | Code | `0x7C440` | `0x38D0` | `0x1D10` |
| 93 (`0x5D`) | `Code93:12E0` | Code | `0x813C0` | `0x20EA` | `0x1D10` |
| 94 (`0x5E`) | `Code94:12E8` | Code | `0x83660` | `0x854` | `0x1D10` |
| 95 (`0x5F`) | `Code95:12F0` | Code | `0x83F60` | `0x78A` | `0x1D10` |
| 96 (`0x60`) | `Code96:12F8` | Code | `0x847A0` | `0x18DE` | `0x1D10` |
| 97 (`0x61`) | `Code97:1300` | Code | `0x86260` | `0x185E` | `0x1D10` |
| 98 (`0x62`) | `Code98:1308` | Code | `0x87C80` | `0x118` | `0x1D10` |
| 99 (`0x63`) | `Code99:1310` | Code | `0x87DE0` | `0x2E` | `0x1C10` |
| 100 (`0x64`) | `Code100:1318` | Code | `0x87E20` | `0xB12` | `0x1D10` |
| 101 (`0x65`) | `Code101:1320` | Code | `0x88A00` | `0xFB0` | `0x1D10` |
| 102 (`0x66`) | `Code102:1328` | Code | `0x89AC0` | `0x14FA` | `0x1D10` |
| 103 (`0x67`) | `Code103:1330` | Code | `0x8B1C0` | `0xE0A` | `0x1D10` |
| 104 (`0x68`) | `Code104:1338` | Code | `0x8C200` | `0xD4A` | `0x1D10` |
| 105 (`0x69`) | `Code105:1340` | Code | `0x8D060` | `0xA7C` | `0x1D10` |
| 106 (`0x6A`) | `Code106:1348` | Code | `0x8DBE0` | `0x1E8` | `0x1D10` |
| 107 (`0x6B`) | `Code107:1350` | Code | `0x8DE40` | `0x56C` | `0x1D10` |
| 108 (`0x6C`) | `Code108:1358` | Code | `0x8E480` | `0x2D8` | `0x1D10` |
| 109 (`0x6D`) | `Code109:1360` | Code | `0x8E7E0` | `0x560` | `0x1D10` |
| 110 (`0x6E`) | `Code110:1368` | Code | `0x8EE20` | `0x122A` | `0x1D10` |
| 111 (`0x6F`) | `Code111:1370` | Code | `0x902A0` | `0x4D4` | `0x1D10` |
| 112 (`0x70`) | `Code112:1378` | Code | `0x907E0` | `0x1A98` | `0x1D10` |
| 113 (`0x71`) | `Code113:1380` | Code | `0x92420` | `0x498` | `0x1D10` |
| 114 (`0x72`) | `Code114:1388` | Code | `0x92920` | `0xF2E` | `0x1D10` |
| 115 (`0x73`) | `Code115:1390` | Code | `0x93900` | `0x197A` | `0x1D10` |
| 116 (`0x74`) | `Code116:1398` | Code | `0x95520` | `0x720` | `0x1D10` |
| 117 (`0x75`) | `Code117:13A0` | Code | `0x95DA0` | `0x140` | `0x1D10` |
| 118 (`0x76`) | `Code118:13A8` | Code | `0x95F20` | `0x2FE` | `0x1D10` |
| 119 (`0x77`) | `Code119:13B0` | Code | `0x962A0` | `0x136` | `0x1D10` |
| 120 (`0x78`) | `Code120:13B8` | Code | `0x96420` | `0x1D4` | `0x1D10` |
| 121 (`0x79`) | `Code121:13C0` | Code | `0x96620` | `0xDF8` | `0x1D10` |
| 122 (`0x7A`) | `Code122:13C8` | Code | `0x974C0` | `0x9F2` | `0x1D10` |
| 123 (`0x7B`) | `Code123:13D0` | Code | `0x97F80` | `0xB50` | `0x1D10` |
| 124 (`0x7C`) | `Code124:13D8` | Code | `0x98B60` | `0x2C2A` | `0x1D10` |
| 125 (`0x7D`) | `Code125:13E0` | Code | `0x9BA80` | `0x516A` | `0x1D10` |
| 126 (`0x7E`) | `Code126:13E8` | Code | `0xA0F20` | `0x100` | `0x1D10` |
| 127 (`0x7F`) | `Code127:13F0` | Code | `0xA1060` | `0x24EA` | `0x1D10` |
| 128 (`0x80`) | `Code128:13F8` | Code | `0xA36C0` | `0x2242` | `0x1D10` |
| 129 (`0x81`) | `Code129:1400` | Code | `0xA5AC0` | `0x14C6` | `0x1D10` |
| 130 (`0x82`) | `Code130:1408` | Code | `0xA7100` | `0xC0C` | `0x1D10` |
| 131 (`0x83`) | `Code131:1410` | Code | `0xA7DA0` | `0x1C6` | `0x1D10` |
| 132 (`0x84`) | `Code132:1418` | Code | `0xA7FA0` | `0x974` | `0x1D10` |
| 133 (`0x85`) | `Code133:1420` | Code | `0xA8980` | `0x140` | `0x1D10` |
| 134 (`0x86`) | `Code134:1428` | Code | `0xA8AE0` | `0x8D8` | `0x1D10` |
| 135 (`0x87`) | `Code135:1430` | Code | `0xA9400` | `0xE4` | `0x1C10` |
| 136 (`0x88`) | `Code136:1438` | Code | `0xA9500` | `0x26A` | `0x1D10` |
| 137 (`0x89`) | `Code137:1440` | Code | `0xA97E0` | `0x1DA` | `0x1D10` |
| 138 (`0x8A`) | `Code138:1448` | Code | `0xA99E0` | `0x227` | `0x1C10` |
| 139 (`0x8B`) | `Data139:1450` | Data | `0xA9C20` | `0x4250` | `0x0D51` |

## TB80UTL.DLL.html

Entry NE 4 at `1018:0526`. Auto data NE 32 at `10F8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x1000` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1A20` | `0x84C` | `0x0D60` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x2340` | `0x3C` | `0x0D60` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x23A0` | `0x3217` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x5DA0` | `0x844` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x6600` | `0x56` | `0x1C70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x6660` | `0x488` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x6B60` | `0xFB0` | `0x1D70` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x7BA0` | `0x1CE` | `0x1D70` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x7DC0` | `0x7DA` | `0x1C70` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x85A0` | `0x18` | `0x1C70` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x85C0` | `0x11E` | `0x1D70` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x8700` | `0x48A` | `0x1D70` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x8EA0` | `0x17C` | `0x1D70` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x9040` | `0x168` | `0x1D70` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x9280` | `0xCBA` | `0x1D70` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x9FA0` | `0xA30` | `0x1D70` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xAA40` | `0x88E` | `0x1D70` |
| 19 (`0x13`) | `Code19:1090` | Code | `0xB360` | `0x3A` | `0x1D70` |
| 20 (`0x14`) | `Code20:1098` | Code | `0xB3C0` | `0x132` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0xB520` | `0xBA` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0xB620` | `0x5CE` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xBC80` | `0x25C` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xBF00` | `0xEC6` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0xCE60` | `0x3E2` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0xD280` | `0x8D8` | `0x1D30` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0xDBA0` | `0x140` | `0x1D30` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0xDD00` | `0x1C0` | `0x1D30` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0xDF00` | `0x3A` | `0x1D30` |
| 30 (`0x1E`) | `Data30:10E8` | Data | `0xDF60` | `0x200` | `0x0C71` |
| 31 (`0x1F`) | `Data31:10F0` | Data | `0xE160` | `0x6` | `0x0C71` |
| 32 (`0x20`) | `Data32:10F8` | Data | `0xE180` | `0x1AB0` | `0x0D71` |

## TB80VBX.DLL.html

Entry NE 2 at `1008:00DA`. Auto data NE 47 at `1170`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xC60` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1680` | `0x2123` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x39C0` | `0x3C` | `0x0D40` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x3A20` | `0x179` | `0x1D10` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x3C40` | `0x153A` | `0x1D10` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x5340` | `0x1EA` | `0x1D10` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x5560` | `0x664` | `0x1D10` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x5C60` | `0x1BF0` | `0x1D10` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x7960` | `0xD86` | `0x1D10` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x87C0` | `0xA94` | `0x1D10` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x9280` | `0x3B8` | `0x1D10` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x9660` | `0x1D6A` | `0x1D10` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0xB640` | `0x4F6` | `0x1D10` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0xBBA0` | `0x27C` | `0x1D10` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0xBE40` | `0x41A` | `0x1D10` |
| 16 (`0x10`) | `Code16:1078` | Code | `0xC2C0` | `0x5DC` | `0x1D10` |
| 17 (`0x11`) | `Code17:1080` | Code | `0xC8E0` | `0x160` | `0x1D10` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xCA60` | `0x1242` | `0x1D10` |
| 19 (`0x13`) | `Code19:1090` | Code | `0xDDC0` | `0x6E4` | `0x1D10` |
| 20 (`0x14`) | `Code20:1098` | Code | `0xE4E0` | `0x132` | `0x1D10` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0xE640` | `0x9AA` | `0x1D10` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0xF0C0` | `0xC77` | `0x1D10` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xFDC0` | `0x1A2` | `0x1D10` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xFFA0` | `0x130` | `0x1D10` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x10120` | `0x1B4` | `0x1D10` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x10300` | `0x56` | `0x1D10` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x10360` | `0x9A` | `0x1D10` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x10420` | `0x38FE` | `0x1D10` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x13EC0` | `0x12FE` | `0x1D10` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x15260` | `0x46` | `0x1D10` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x152E0` | `0x4C` | `0x1C10` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x15340` | `0x68E` | `0x1D10` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x15A80` | `0x2C4` | `0x1D10` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x15DA0` | `0xB74` | `0x1D10` |
| 35 (`0x23`) | `Code35:1110` | Code | `0x169E0` | `0x3AC` | `0x1D10` |
| 36 (`0x24`) | `Code36:1118` | Code | `0x16E20` | `0x528` | `0x1D10` |
| 37 (`0x25`) | `Code37:1120` | Code | `0x173E0` | `0xE88` | `0x1D10` |
| 38 (`0x26`) | `Code38:1128` | Code | `0x18320` | `0x78C` | `0x1D10` |
| 39 (`0x27`) | `Code39:1130` | Code | `0x18AE0` | `0x107A` | `0x1D10` |
| 40 (`0x28`) | `Code40:1138` | Code | `0x19BE0` | `0x248` | `0x1D10` |
| 41 (`0x29`) | `Code41:1140` | Code | `0x19E60` | `0x3A` | `0x1C10` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0x19EA0` | `0xA20` | `0x1D10` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0x1A920` | `0x19E` | `0x1D10` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0x1AAE0` | `0x1C20` | `0x1D10` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0x1C720` | `0x370` | `0x1D10` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0x1CAA0` | `0xF0` | `0x1D10` |
| 47 (`0x2F`) | `Data47:1170` | Data | `0x1CBE0` | `0x2778` | `0x0D71` |

## TB80W16.DLL.html

Entry NE 3 at `1010:027A`. Auto data NE 56 at `11B8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x3CE0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x4700` | `0x3C` | `0x0D60` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x4760` | `0x1FF9` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x6800` | `0x6E` | `0x1D70` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x68A0` | `0x654` | `0x1D70` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x6F40` | `0x234` | `0x1D70` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x71C0` | `0x916` | `0x1D70` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x7B40` | `0xD30` | `0x1D30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x8940` | `0x50A` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x8EA0` | `0x49C` | `0x1D30` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x9380` | `0x14FE` | `0x1D30` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0xA8E0` | `0x2AF0` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0xD4C0` | `0xFE` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0xD600` | `0xA42` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0xE0C0` | `0x1D6` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0xE2C0` | `0x53A` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0xE860` | `0xCA2` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xF560` | `0xB7E` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x10120` | `0x68A` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x107E0` | `0x4CBE` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x15500` | `0x1CE8` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x17380` | `0x770` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0x17B40` | `0x3470` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0x1B0E0` | `0x25C` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0x1B380` | `0x3CC` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x1B7A0` | `0x2D2` | `0x1D30` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x1BAC0` | `0x4E6` | `0x1D30` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x1C000` | `0x4E8` | `0x1D30` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x1C520` | `0x582` | `0x1D30` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x1CB20` | `0x8D8` | `0x1D30` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0x1D440` | `0x268` | `0x1D30` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0x1D720` | `0x140` | `0x1D30` |
| 33 (`0x21`) | `Code33:1100` | Code | `0x1D880` | `0x1C0` | `0x1D30` |
| 34 (`0x22`) | `Code34:1108` | Code | `0x1DA80` | `0x1234` | `0x1D30` |
| 35 (`0x23`) | `Data35:1110` | Data | `0x1ED60` | `0x6` | `0x0C71` |
| 36 (`0x24`) | `Data36:1118` | Data | `0x1ED80` | `0xA` | `0x0C71` |
| 37 (`0x25`) | `Data37:1120` | Data | `0x1EDA0` | `0x8` | `0x0C71` |
| 38 (`0x26`) | `Data38:1128` | Data | `0x1EDC0` | `0xA` | `0x0C71` |
| 39 (`0x27`) | `Data39:1130` | Data | `0x1EDE0` | `0x8` | `0x0C71` |
| 40 (`0x28`) | `Data40:1138` | Data | `0x1EE00` | `0x8` | `0x0C71` |
| 41 (`0x29`) | `Data41:1140` | Data | `0x1EE20` | `0xA` | `0x0C71` |
| 42 (`0x2A`) | `Data42:1148` | Data | `0x1EE40` | `0x24` | `0x0C71` |
| 43 (`0x2B`) | `Data43:1150` | Data | `0x1EE80` | `0x10` | `0x0C71` |
| 44 (`0x2C`) | `Data44:1158` | Data | `0x1EEA0` | `0x14` | `0x0C71` |
| 45 (`0x2D`) | `Data45:1160` | Data | `0x1EEC0` | `0xA` | `0x0C71` |
| 46 (`0x2E`) | `Data46:1168` | Data | `0x1EEE0` | `0xA` | `0x0C71` |
| 47 (`0x2F`) | `Data47:1170` | Data | `0x1EF00` | `0x8` | `0x0C71` |
| 48 (`0x30`) | `Data48:1178` | Data | `0x1EF20` | `0x8` | `0x0C71` |
| 49 (`0x31`) | `Data49:1180` | Data | `0x1EF40` | `0x1C` | `0x0C71` |
| 50 (`0x32`) | `Data50:1188` | Data | `0x1EF60` | `0x8` | `0x0C71` |
| 51 (`0x33`) | `Data51:1190` | Data | `0x1EF80` | `0xA` | `0x0C71` |
| 52 (`0x34`) | `Data52:1198` | Data | `0x1EFA0` | `0x10` | `0x0C71` |
| 53 (`0x35`) | `Data53:11A0` | Data | `0x1EFC0` | `0xA` | `0x0C71` |
| 54 (`0x36`) | `Data54:11A8` | Data | `0x1EFE0` | `0xA` | `0x0C71` |
| 55 (`0x37`) | `Data55:11B0` | Data | `0x1F000` | `0x8` | `0x0C71` |
| 56 (`0x38`) | `Data56:11B8` | Data | `0x1F020` | `0x2194` | `0x0D71` |

## TBCBT.DLL.html

Entry NE 2 at `1008:0054`. Auto data NE 16 at `1078`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x760` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1180` | `0x232B` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x3880` | `0x80` | `0x1D30` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x3940` | `0xE8` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x3A60` | `0x296` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x3D60` | `0xFD8` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x4F80` | `0x11F0` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x6200` | `0x7A6` | `0x1D30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x6A40` | `0x748` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x7200` | `0x1996` | `0x1D30` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x8D00` | `0x8A2` | `0x1D30` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x9620` | `0x59E` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x9C00` | `0xDD6` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0xAC00` | `0x4D4` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0xB160` | `0x1C4` | `0x1D30` |
| 16 (`0x10`) | `Data16:1078` | Data | `0xB380` | `0x296E` | `0x0D71` |

## TBDB3.DLL.html

Entry NE 2 at `1008:0628`. Auto data NE 72 at `1238`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xA00` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1420` | `0x32DC` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x4C40` | `0x3C` | `0x0D60` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x4CA0` | `0x76C` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x5460` | `0x96C` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x5EA0` | `0x90A` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x6820` | `0x126` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x6980` | `0x2C` | `0x1C30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x69C0` | `0x82` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x6A60` | `0x6E` | `0x1D30` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x6AE0` | `0x38` | `0x1C30` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x6B20` | `0x142` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x6CA0` | `0x280` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x6FA0` | `0x7AE` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x7800` | `0x336` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x7BA0` | `0xABA` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x86C0` | `0x318` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0x8A40` | `0x152` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0x8C00` | `0xE6` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0x8D00` | `0x46` | `0x1C30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0x8D60` | `0x716` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0x9500` | `0xC4A` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xA220` | `0x106` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xA360` | `0x43E` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0xA820` | `0x352` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0xABE0` | `0x258` | `0x1D30` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0xAE80` | `0x23A` | `0x1D30` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0xB140` | `0x3FA` | `0x1D30` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0xB5A0` | `0x116` | `0x1D30` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0xB6E0` | `0x1098` | `0x1D30` |
| 31 (`0x1F`) | `Code31:10F0` | Code | `0xC860` | `0xEA` | `0x1D30` |
| 32 (`0x20`) | `Code32:10F8` | Code | `0xC960` | `0x63C` | `0x1D30` |
| 33 (`0x21`) | `Code33:1100` | Code | `0xCFC0` | `0x848` | `0x1D30` |
| 34 (`0x22`) | `Code34:1108` | Code | `0xD8E0` | `0xF0` | `0x1D30` |
| 35 (`0x23`) | `Code35:1110` | Code | `0xDA20` | `0xF6` | `0x1D30` |
| 36 (`0x24`) | `Code36:1118` | Code | `0xDB60` | `0x168` | `0x1D30` |
| 37 (`0x25`) | `Code37:1120` | Code | `0xDD20` | `0xAA` | `0x1D30` |
| 38 (`0x26`) | `Code38:1128` | Code | `0xDDE0` | `0x8A` | `0x1D30` |
| 39 (`0x27`) | `Code39:1130` | Code | `0xDEA0` | `0xCA` | `0x1D30` |
| 40 (`0x28`) | `Code40:1138` | Code | `0xDFA0` | `0x21C` | `0x1D30` |
| 41 (`0x29`) | `Code41:1140` | Code | `0xE200` | `0xAA` | `0x1D30` |
| 42 (`0x2A`) | `Code42:1148` | Code | `0xE2C0` | `0x20C` | `0x1D30` |
| 43 (`0x2B`) | `Code43:1150` | Code | `0xE560` | `0x94` | `0x1D30` |
| 44 (`0x2C`) | `Code44:1158` | Code | `0xE620` | `0x24` | `0x1C30` |
| 45 (`0x2D`) | `Code45:1160` | Code | `0xE660` | `0x76E` | `0x1D30` |
| 46 (`0x2E`) | `Code46:1168` | Code | `0xEE80` | `0x47C` | `0x1D30` |
| 47 (`0x2F`) | `Code47:1170` | Code | `0xF340` | `0xBC` | `0x1D30` |
| 48 (`0x30`) | `Code48:1178` | Code | `0xF420` | `0x660` | `0x1D30` |
| 49 (`0x31`) | `Code49:1180` | Code | `0xFAE0` | `0x192` | `0x1D30` |
| 50 (`0x32`) | `Code50:1188` | Code | `0xFCA0` | `0xA6C` | `0x1D30` |
| 51 (`0x33`) | `Code51:1190` | Code | `0x107A0` | `0xC6` | `0x1D30` |
| 52 (`0x34`) | `Code52:1198` | Code | `0x10880` | `0x19E` | `0x1D30` |
| 53 (`0x35`) | `Code53:11A0` | Code | `0x10A40` | `0x16A` | `0x1D30` |
| 54 (`0x36`) | `Code54:11A8` | Code | `0x10BE0` | `0x82` | `0x1D30` |
| 55 (`0x37`) | `Code55:11B0` | Code | `0x10C80` | `0xCE` | `0x1D30` |
| 56 (`0x38`) | `Code56:11B8` | Code | `0x10D80` | `0x264` | `0x1C30` |
| 57 (`0x39`) | `Code57:11C0` | Code | `0x11000` | `0x110` | `0x1D30` |
| 58 (`0x3A`) | `Code58:11C8` | Code | `0x11140` | `0x16` | `0x1C30` |
| 59 (`0x3B`) | `Code59:11D0` | Code | `0x11160` | `0x50` | `0x1C30` |
| 60 (`0x3C`) | `Code60:11D8` | Code | `0x111C0` | `0x16` | `0x1C30` |
| 61 (`0x3D`) | `Code61:11E0` | Code | `0x111E0` | `0x99A` | `0x1D30` |
| 62 (`0x3E`) | `Code62:11E8` | Code | `0x11BC0` | `0xEE6` | `0x1D30` |
| 63 (`0x3F`) | `Code63:11F0` | Code | `0x12C80` | `0xB4E` | `0x1D30` |
| 64 (`0x40`) | `Code64:11F8` | Code | `0x13820` | `0x94` | `0x1C30` |
| 65 (`0x41`) | `Code65:1200` | Code | `0x138C0` | `0xE34` | `0x1D30` |
| 66 (`0x42`) | `Code66:1208` | Code | `0x147A0` | `0x4E` | `0x1D30` |
| 67 (`0x43`) | `Code67:1210` | Code | `0x14800` | `0x1C4` | `0x1D30` |
| 68 (`0x44`) | `Code68:1218` | Code | `0x14A20` | `0x8A2` | `0x1D30` |
| 69 (`0x45`) | `Code69:1220` | Code | `0x15340` | `0x59E` | `0x1D30` |
| 70 (`0x46`) | `Data70:1228` | Data | `0x15920` | `0x107` | `0x0C71` |
| 71 (`0x47`) | `Data71:1230` | Data | `0x15A40` | `0x114` | `0x0C71` |
| 72 (`0x48`) | `Data72:1238` | Data | `0x15B60` | `0x17D8` | `0x0D71` |

## TBDLG.DLL.html

Entry NE 17 at `1080:027A`. Auto data NE 19 at `1090`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xA60` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1480` | `0x3C` | `0x0D40` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x14E0` | `0x1A7C` | `0x1D50` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x30E0` | `0x5BE` | `0x1D50` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x3700` | `0x18C` | `0x1D50` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x38C0` | `0x336` | `0x1D50` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x3C40` | `0x78A` | `0x1D50` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x4420` | `0x374` | `0x1D50` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x4820` | `0x1DC` | `0x1D50` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x4A40` | `0xC56` | `0x1D50` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x5780` | `0x263A` | `0x1D50` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x7F60` | `0x4A2` | `0x1D50` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x8440` | `0x290` | `0x1D50` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x87A0` | `0xAC` | `0x1D50` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x8860` | `0x8A2` | `0x1D50` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x9180` | `0x59E` | `0x1D50` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x9760` | `0xC75` | `0x1D50` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xA4A0` | `0x748` | `0x1D50` |
| 19 (`0x13`) | `Data19:1090` | Data | `0xAC60` | `0x9821` | `0x0C71` |

## TBDOS.DLL.html

Entry NE 2 at `1008:027A`. Auto data NE 7 at `1030`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x560` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xF80` | `0xCE3` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x1D40` | `0x3C` | `0x0D60` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x1DA0` | `0x2C1A` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x4B00` | `0x59E` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x50E0` | `0x8A2` | `0x1D30` |
| 7 (`0x07`) | `Data7:1030` | Data | `0x5A00` | `0x1792` | `0x0D71` |

## TBFILE32.DLL.html

Entry NE 3 at `1010:0054`. Auto data NE 9 at `1040`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x760` | `0x1F82` | `0x1D70` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x27C0` | `0x54` | `0x0D60` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x2840` | `0xAB8` | `0x1D70` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x36C0` | `0x4A` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x3720` | `0xC0E` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x43C0` | `0x8D8` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x4CE0` | `0x13F` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x4E40` | `0x1C3` | `0x1D30` |
| 9 (`0x09`) | `Data9:1040` | Data | `0x33A0` | `0x2E6` | `0x0C71` |

## TBPDX.DLL.html

Entry NE 4 at `1018:0068`. Auto data NE 5 at `1020`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0xC00` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1620` | `0x3C` | `0x0D40` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x1680` | `0x6E56` | `0x1D50` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x8A20` | `0x1E85` | `0x1D50` |
| 5 (`0x05`) | `Data5:1020` | Data | `0xAAA0` | `0x940` | `0x0D71` |

## TBREG.DLL.html

Entry NE 2 at `1008:0064`. Auto data NE 11 at `1050`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x2A0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xCC0` | `0x1D21` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x2AA0` | `0x3C` | `0x0D60` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x2B00` | `0x224` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x2D40` | `0x3EBE` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x6D20` | `0x18A` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x6EE0` | `0x510` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x7420` | `0x8A` | `0x1D30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x74E0` | `0x1DA` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x76E0` | `0x29C` | `0x1D30` |
| 11 (`0x0B`) | `Data11:1050` | Data | `0x79A0` | `0x5D2` | `0x0D71` |

## TBWIN.DLL.html

Entry NE 2 at `1008:0946`. Auto data NE 28 at `10D8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x920` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1340` | `0x2597` | `0x1D70` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x3D00` | `0x3C` | `0x0D60` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x3D60` | `0x4D4` | `0x1D30` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x42C0` | `0xBEC` | `0x1D30` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x51A0` | `0x968` | `0x1D30` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x5B60` | `0x124` | `0x1D30` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x5CA0` | `0x87C` | `0x1D30` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x65A0` | `0x7C2` | `0x1D30` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x6DE0` | `0x224` | `0x1D30` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x7060` | `0x5CE` | `0x1D30` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x76E0` | `0xDD6` | `0x1D30` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x86E0` | `0x7F4` | `0x1D30` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x8F60` | `0x5D4` | `0x1D30` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x9600` | `0x7A` | `0x1D30` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x96A0` | `0x8A2` | `0x1D30` |
| 17 (`0x11`) | `Code17:1080` | Code | `0x9FC0` | `0x59E` | `0x1D30` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xA5A0` | `0xAC` | `0x1D30` |
| 19 (`0x13`) | `Code19:1090` | Code | `0xA660` | `0x268` | `0x1D30` |
| 20 (`0x14`) | `Code20:1098` | Code | `0xA940` | `0x1C0` | `0x1D30` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0xAB40` | `0x8D8` | `0x1D30` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0xB460` | `0x140` | `0x1D30` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xB5C0` | `0x1C4` | `0x1D30` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xB7E0` | `0xFD8` | `0x1D30` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0xCA00` | `0x748` | `0x1D30` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0xD1C0` | `0xE8` | `0x1D30` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0xD2E0` | `0x7A6` | `0x1D30` |
| 28 (`0x1C`) | `Data28:10D8` | Data | `0xDB20` | `0x3EAE` | `0x0D71` |

## decrypt.exe.html

Entry NE 2 at `1008:15A4`. Auto data NE 3 at `1010`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x2A0` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0xCC0` | `0x205A` | `0x1D50` |
| 3 (`0x03`) | `Data3:1010` | Data | `0x2EA0` | `0xFA0` | `0x0C51` |

## TB80OLE.DLL

Entry NE 2 at `1008:0054`. Auto data NE 32 at `10F8`.

| NE | Ghidra | Kind | File offset | Length | Flags |
|---|---|---|---:|---:|---|
| 1 (`0x01`) | `Code1:1000` | Code | `0x1040` | `0x9F2` | `0x0D50` |
| 2 (`0x02`) | `Code2:1008` | Code | `0x1A60` | `0xAD9` | `0x1D50` |
| 3 (`0x03`) | `Code3:1010` | Code | `0x25E0` | `0x3C` | `0x0D40` |
| 4 (`0x04`) | `Code4:1018` | Code | `0x2640` | `0x10` | `0x1C10` |
| 5 (`0x05`) | `Code5:1020` | Code | `0x2660` | `0x60` | `0x1D10` |
| 6 (`0x06`) | `Code6:1028` | Code | `0x2700` | `0x8D6` | `0x1D10` |
| 7 (`0x07`) | `Code7:1030` | Code | `0x30C0` | `0x25A` | `0x1D10` |
| 8 (`0x08`) | `Code8:1038` | Code | `0x3360` | `0x2EBC` | `0x1D10` |
| 9 (`0x09`) | `Code9:1040` | Code | `0x63C0` | `0x270` | `0x1D10` |
| 10 (`0x0A`) | `Code10:1048` | Code | `0x66A0` | `0x384` | `0x1D10` |
| 11 (`0x0B`) | `Code11:1050` | Code | `0x6A40` | `0x490` | `0x1D10` |
| 12 (`0x0C`) | `Code12:1058` | Code | `0x6F40` | `0x6CE` | `0x1D10` |
| 13 (`0x0D`) | `Code13:1060` | Code | `0x7640` | `0x594` | `0x1D10` |
| 14 (`0x0E`) | `Code14:1068` | Code | `0x7C40` | `0x1F2` | `0x1D10` |
| 15 (`0x0F`) | `Code15:1070` | Code | `0x7E60` | `0x7B0` | `0x1D10` |
| 16 (`0x10`) | `Code16:1078` | Code | `0x8700` | `0x219A` | `0x1D10` |
| 17 (`0x11`) | `Code17:1080` | Code | `0xAAA0` | `0xE6A` | `0x1D10` |
| 18 (`0x12`) | `Code18:1088` | Code | `0xBA60` | `0x1D96` | `0x1D10` |
| 19 (`0x13`) | `Code19:1090` | Code | `0xD980` | `0x18A` | `0x1D10` |
| 20 (`0x14`) | `Code20:1098` | Code | `0xDB80` | `0xDC4` | `0x1D10` |
| 21 (`0x15`) | `Code21:10A0` | Code | `0xEA60` | `0x44A` | `0x1D10` |
| 22 (`0x16`) | `Code22:10A8` | Code | `0xEF80` | `0x21C` | `0x1D10` |
| 23 (`0x17`) | `Code23:10B0` | Code | `0xF200` | `0x77E` | `0x1D10` |
| 24 (`0x18`) | `Code24:10B8` | Code | `0xFA20` | `0x3CC` | `0x1D10` |
| 25 (`0x19`) | `Code25:10C0` | Code | `0xFEA0` | `0x436` | `0x1D10` |
| 26 (`0x1A`) | `Code26:10C8` | Code | `0x103C0` | `0x228` | `0x1D10` |
| 27 (`0x1B`) | `Code27:10D0` | Code | `0x10680` | `0xC0E` | `0x1D10` |
| 28 (`0x1C`) | `Code28:10D8` | Code | `0x11320` | `0x8D8` | `0x1D10` |
| 29 (`0x1D`) | `Code29:10E0` | Code | `0x11C40` | `0x140` | `0x1D10` |
| 30 (`0x1E`) | `Code30:10E8` | Code | `0x11DA0` | `0x108` | `0x1D10` |
| 31 (`0x1F`) | `Data31:10F0` | Data | `0x11EE0` | `0x6` | `0x0C71` |
| 32 (`0x20`) | `Data32:10F8` | Data | `0x11F00` | `0xC8E` | `0x0D71` |


# TB80RTM NE segment to Ghidra space

> Trail, 2026-10-16. Lookup. NE segment to the Ghidra base used for this load. Not a finding. A live selector is not this base. If this file and `TBdecompile/record/` disagree, the record wins.

| NE | Ghidra |
|----|--------|
| 0x01 | 1000 |
| 0x02 | 1008 |
| 0x03 | 1010 |
| 0x04 | 1018 |
| 0x05 | 1020 |
| 0x06 | 1028 |
| 0x07 | 1030 |
| 0x08 | 1038 |
| 0x09 | 1040 |
| 0x0A | 1048 |
| 0x0B | 1050 |
| 0x0C | 1058 |
| 0x0D | 1060 |
| 0x0E | 1068 |
| 0x0F | 1070 |
| 0x10 | 1078 |
| 0x11 | 1080 |
| 0x12 | 1088 |
| 0x13 | 1090 |
| 0x14 | 1098 |
| 0x15 | 10A0 |
| 0x16 | 10A8 |
| 0x17 | 10B0 |
| 0x18 | 10B8 |
| 0x19 | 10C0 |
| 0x1A | 10C8 |
| 0x1B | 10D0 |
| 0x1C | 10D8 |
| 0x1D | 10E0 |
| 0x1E | 10E8 |
| 0x1F | 10F0 |
| 0x20 | 10F8 |
| 0x21 | 1100 |
| 0x22 | 1108 |
| 0x23 | 1110 |
| 0x24 | 1118 |
| 0x25 | 1120 |
| 0x26 | 1128 |
| 0x27 | 1130 |
| 0x28 | 1138 |
| 0x29 | 1140 |
| 0x2A | 1148 |
| 0x2B | 1150 |
| 0x2C | 1158 |
| 0x2D | 1168 |
| 0x2E | 1170 |
| 0x2F | 1178 |
| 0x30 | 1180 |
| 0x31 | 1188 |
| 0x32 | 1190 |
| 0x33 | 1198 |
| 0x34 | 11A0 |
| 0x35 | 11A8 |
| 0x36 | 11B0 |
| 0x37 | 11B8 |
| 0x38 | 11C0 |
| 0x39 | 11D0 |
| 0x3A | 11D8 |
| 0x3B | 11E0 |
| 0x3C | 11E8 |
| 0x3D | 11F0 |
| 0x3E | 11F8 |
| 0x3F | 1200 |
| 0x40 | 1208 |
| 0x41 | 1210 |
| 0x42 | 1218 |
| 0x43 | 1220 |
| 0x44 | 1228 |
| 0x45 | 1230 |
| 0x46 | 1238 |
| 0x47 | 1240 |
| 0x48 | 1248 |
| 0x49 | 1250 |
| 0x4A | 1258 |
| 0x4B | 1260 |
| 0x4C | 1268 |
| 0x4D | 1270 |
| 0x4E | 1278 |
| 0x4F | 1280 |
| 0x50 | 1288 |
| 0x51 | 1290 |
| 0x52 | 1298 |
| 0x53 | 12A0 |
| 0x54 | 12A8 |
| 0x55 | 12B0 |
| 0x56 | 12B8 |
| 0x57 | 12C0 |
| 0x58 | 12D0 |
| 0x59 | 12D8 |
| 0x5A | 12E0 |
| 0x5B | 12E8 |
| 0x5C | 12F0 |
| 0x5D | 12F8 |
| 0x5E | 1300 |
| 0x5F | 1310 |
| 0x60 | 1318 |
| 0x61 | 1320 |
| 0x62 | 1328 |
| 0x63 | 1330 |
| 0x64 | 1338 |
| 0x65 | 1340 |
| 0x66 | 1348 |
| 0x67 | 1350 |
| 0x68 | 1358 |
| 0x69 | 1360 |
| 0x6A | 1368 |
| 0x6B | 1370 |
| 0x6C | 1378 |
| 0x6D | 1380 |
| 0x6E | 1388 |
| 0x6F | 1390 |
| 0x70 | 1398 |
| 0x71 | 13A0 |
| 0x72 | 13A8 |
| 0x73 | 13B0 |
| 0x74 | 13B8 |
| 0x75 | 13C0 |
| 0x76 | 13C8 |
| 0x77 | 13D0 |
| 0x78 | 13D8 |
| 0x79 | 13E0 |
| 0x7A | 13E8 |
| 0x7B | 13F0 |
| 0x7C | 13F8 |
| 0x7D | 1400 |
| 0x7E | 1408 |
| 0x7F | 1410 |
| 0x80 | 1418 |
| 0x81 | 1420 |
| 0x82 | 1428 |
| 0x83 | 1430 |
| 0x84 | 1438 |
| 0x85 | 1440 |
| 0x86 | 1448 |


# WDW selector:offset → Ghidra segment:offset

> Trail, 2026-10-16. Lookup. One boot's WDW selectors. They change on the next boot. If this file and `TBdecompile/record/` disagree, the record wins.

Source: WDW screenshots 2026-10-15. Live selectors are temporary (this boot). Offsets within the segment are stable. Map is tbworkingpapers/tbwp0002/TB80BAS.map. C decompile is Toolbook/_decompiles/TB80BAS.DLL.c.

## Resolved (in map)

| WDW (this boot) | Export | Ghidra | Notes |
|-----------------|--------|--------|-------|
| 4877:0000 | CDBDISPLAYSTATE | 1008:4B4A | display state |
| 483F:03B2 | CDBCREATEPAGEREF | 1010:211C | create page ref; calls FUN_1048_159a(...,2,...) |
| 3397:147C | CDBSETVALUEEX | 1048:2F0E | set property value; cmp [bp+0E],42 then sub ax,4000 |
| 3767:0000 | CDBREGISTEROLE2WINDOW | 1310:0292 | register OLE2 window |
| — | CDBNEWOBJECT | 12C8:0850 | object create (FUN_12c8_0850) |
| — | CDBFILEOPEN | 1028:1226 | file open |

## In C decompile, not in map (look up by name in Ghidra)

| Export | C line | Distinctive pattern from screenshot |
|--------|--------|-------------------------------------|
| CDBSYNCSCREENS | 12922 | DAT_1630_3048 = 0; DAT_1630_304a = param |
| CDBCLEARBOOKREFS | 28451 | enter 0xB8; lea ax,-2E[bp] |
| CDBCLIENTSTATUS | 25257 | push [bp+08]; push [bp+06]; push 1; call far |
| CDBREGISTERINSTWINDOW | 25296 | mov bx,[bp+0E]; mov byte [bx],0 |
| CDBREGISTERVBXFORM | 129508 | enter 6; mov bx,[bp+08]; push 1 |
| VBXNEWVIEW | 129713 | enter 8; push 011C; call far |
| VALUEARRAYINFO | 87815 | mov al,[bp+0D]; and al,FC; cmp al,44 |
| VALUEARRAYGET | 87982 | mov al,[bp+0A]; sub ah,ah |
| VALUEARRAYSET | 88133 | les bx,[bp+14]; mov ax,es:[bx+0C] |
| HEAPVALUETOPOINTER | (calls) | and si,03FF; add si,si |
| HEAPVALUETOFRAME | (calls) | push [bp+0C]; push [bp+0A]; push [bp+08]; push [bp+06] |
| OBJGETFILE | (calls) | enter 14; mov bx,[bp+0A]; mov byte [bx],0 |
| OBJGETHDRLONG | (calls) | enter 2; mov word 2862,ax |

## Call stack spine (book-open / page path)

These frames appear in nearly every Calls window. Selectors are this boot.

```
0x3497:03EF
0x3497:4A6E
0x3197:0379
0x3167:0CB1 → 0x3167:14BC
0x3247:02BF → 0x3247:05B7 → 0x3247:0B7A
```

## Practical

- Break on the Ghidra address by offset within the segment. The live selector is whatever WDW shows for TB80BAS that boot.
- CDBSENDCREATE is listed in the Functions window but did not appear in the Calls stacks. Object creation on this path is going through CDBCREATEPAGEREF / CDBSETVALUEEX / CDBVALUENEW*.
- Clear unused breakpoints. The "Device memory is nearly full" stop is the debugger.

## Next

Set the break on CDBCREATEPAGEREF (Ghidra 1010:211C) or CDBSETVALUEEX (Ghidra 1048:2F0E). Step into the call that builds the page. That is closer to the record reader than waiting for CDBSENDCREATE.

## Startup sequence (this batch)

Stops in order. VALUEFREE fired for the first time before the main window. Next batch ends at VALUETOSTRING before the file dialog.

| Order | WDW this boot | Export | Ghidra (if known) | Notes |
|-------|---------------|--------|-------------------|-------|
| 1 | 483F:041E | CDBVIEWPAGEVALUE | — | view page value |
| 2 | 343F:0876 | LOCKPATTERN | — | lock pattern |
| 3 | 3397:0958 | CDBQUERYVALUE | — | query value |
| 4 | 483F:0666 | CDBCREATEBKGNDREF | — | create background ref |
| 5 | 3397:113C | CDBSENDVALUEEX | — | send value |
| 6 | 450F:0E3E | TBHEAPSAVECRITSECT | — | heap critical section |
| 7 | 336F:0096 | CDBSCRIPTSEARCH | — | script search |
| 8 | 3397:0304 | CDBREFVALUE | — | ref value |
| 9 | 450F:0E70 | TBHEAPRESTORECRITSECT | — | restore crit |
| 10 | 4267:04E0 | CDBVALUEBOOKTOSTRING | — | book to string |
| 11 | 3397:0AAA | CDBQUERYFILEPATH | 1078:036C | query file path |
| 12 | 44D7:0000 | VALUENEWSTRING | — | new string |
| 13 | 450F:0840 | TBHEAPALLOC | — | heap alloc |
| 14 | 450F:0EE2 | HEAPPOINTERTOVALUE | — | pointer to value |
| 15 | 4877:090E | CDBSETIMAGEMEMORYMODEL | — | image memory model |
| 16 | 4D27:1710 | RESMGREXTRACT | — | resource extract |
| 17 | 3397:0612 | CDBBOOKOFVALUE | — | book of value |
| 18 | 3397:1110 | CDBSENDVALUE | — | send value |
| 19 | 4877:0506 | CDBPAINTCLIENT | — | paint client (sets 3048/304A) |
| 20 | 4877:0B6C | IMDRAWLEVELS | 1020:16DE | draw levels |
| 21 | 3AB7:0244 | CDBSETFOCUS | 1060:143E | set focus |
| 22 | 44CF:07CA | CDBSENDUNDO | — | send undo |
| 23 | 4877:09CE | IMBITBLT | — | bitblt |
| 24 | 450F:0EC2 | TBHEAPCLEARCRITSECT | — | clear crit |
| 25 | 381F:0254 | CDBRESETPLERR | — | reset error |
| 26 | 4457:0B38 | VALUEFREE | — | free value (before main window) |

## Observations

- CDBPAINTCLIENT (4877:0506) sets DAT_1630_3048 = 0 and DAT_1630_304A from the stack, same pattern as CDBSYNCSCREENS. Paint is starting before the main window.
- RESMGREXTRACT (4D27:1710) is the resource extractor. It runs before VALUEFREE.
- VALUEFREE at 4457:0B38 is the last first-time stop before the main window. The next batch ends at VALUETOSTRING before the file dialog.
- CDBSENDCREATE still has not appeared in the Calls windows. Object creation on this path is going through CDBCREATEBKGNDREF / CDBCREATEPAGEREF / CDBSETVALUEEX / CDBSENDVALUE.
- Clear unused breakpoints. The "memory and was forced to stop" message is the debugger running out of room.

## Next

The next batch ends at VALUETOSTRING (before the file dialog). Capture that sequence the same way. The record reader is still upstream of CDBSENDCREATE; these stops are the property and resource path that runs while the book is opening.

## Selector → segment mapping

The WDW selector (483F, 3397, 450F, etc.) is temporary. Windows assigns it when the NE segment is loaded. The Ghidra segment number is the NE segment index. They are not the same number.

### How to map this boot

1. In WDW, open the Module window (Window → Module, or the module list).
2. Find TB80BAS.DLL. It shows the selector for each loaded segment.
3. Or: set a break on a known function, then look at the Calls window. The return address selector is the caller's segment.
4. Once you know one selector maps to one Ghidra segment, every other function with that same selector is in the same Ghidra segment.

### Known this boot (from the screenshots)

These selectors appeared. The map offsets do not match the WDW offsets, so the map is from a different Ghidra pass. Use the WDW offset as the stable address.

| WDW selector | Seen on | Notes |
|--------------|---------|-------|
| 483F | CDBVIEWPAGEVALUE, CDBCREATEBKGNDREF | same segment |
| 3397 | CDBQUERYVALUE, CDBSENDVALUEEX, CDBREFVALUE, CDBQUERYFILEPATH, CDBBOOKOFVALUE, CDBSENDVALUE | same segment |
| 450F | TBHEAP* family | heap segment |
| 4877 | CDBSETIMAGEMEMORYMODEL, CDBPAINTCLIENT, IMDRAWLEVELS, IMBITBLT | paint/image segment |
| 4D27 | RESMGREXTRACT | resource segment |
| 4267 | CDBVALUEBOOKTOSTRING | |
| 44D7 | VALUENEWSTRING | |
| 44CF | CDBSENDUNDO | |
| 3AB7 | CDBSETFOCUS | |
| 381F | CDBRESETPLERR | |
| 4457 | VALUEFREE | |
| 336F | CDBSCRIPTSEARCH | |
| 343F | LOCKPATTERN | |

### Practical

- The offset is what matches Ghidra. If the map offset does not match the WDW offset, the map is from a different analysis. Use the WDW offset and the function name.
- To get a fresh map, re-export the Ghidra symbol map from the current analysis.
- Clear unused breakpoints. The debugger is running out of memory.

## Method (this boot)

For each first-time stop we have:

- WDW selector (temporary, changes next boot)
- Function name (stable)
- Offset within the segment (stable)
- First instructions (stable pattern)

Match later by name + offset + instruction bytes. Do not re-scan the whole Functions list. The Calls window already shows the return address of the caller; that is the next place to look if the function is not named.

If the session is restarted, the selector changes. The offset and the instruction bytes do not. Match on those.

## What we have this boot

See the table above. The map offsets do not match the WDW offsets, so the map is from a different analysis. Use the WDW offset and the function name. Re-export the Ghidra symbol map from the current analysis to get fresh offsets.

## Batch 2026-10-15 17:38–17:46

| Function | WDW selector:offset | Segment group | Notes |
|----------|---------------------|---------------|-------|
| VALUETOSTRING | 4457:0DE8 | 4457 | value convert |
| OBJFILEOPEN | 3147:177C | 3147 | file open |
| STACKGETSIZE | 4537:0738 | 4537 | stack |
| VALUENEWSTACK | 4537:0000 | 4537 | stack |
| STACKPUSH | 4537:0778 | 4537 | stack |
| CDBCHUNKLAST | 0D37:0334 | 0D37 | chunk walk |
| CDBCHUNKEND | 0D37:0000 | 0D37 | chunk walk |
| STACKPUSHONE | 4537:09A2 | 4537 | stack |
| STACKELEMENT | 4537:0444 | 4537 | stack |
| STACKSETELEMENT | 4537:06B0 | 4537 | stack |
| VALUENEW | 4457:0C6E | 4457 | value |
| VALUEAS | 4457:0038 | 4457 | value |
| VALUEASEX | 4457:00A0 | 4457 | value |
| RESMGRENUM | 4D27:2522 | 4D27 | resource enum |
| CDBLOCKVALUE | 3397:02CA | 3397 | value lock |
| HEAPCREATEFRAME | 450F:0350 | 450F | heap |
| VALUEASC | 4457:01B8 | 4457 | value |
| VALUEASCEX | 4457:0220 | 4457 | value |
| VALUECONVERTTOC | 4457:0818 | 4457 | value |
| VALUECONVERTTOCEX | 4457:0880 | 4457 | value |
| VALUEFROMSTRING | 4457:0E1A | 4457 | value |
| CDBSETPLERR | 381F:0010 | 381F | error |
| LPSTRTODOUBLE | 4477:05B4 | 4477 | string→double |
| HEAPGETHANDLER | 450F:0FEE | 450F | heap |
| VALUECHECK | 44FF:0000 | 44FF | value |
| CDBCHUNKFIND | 0D37:0146 | 0D37 | chunk walk |
| HEAPRELEASEFRAME | 450F:05D6 | 450F | heap |
| VALUENEWLAYEREX | 4267:127A | 4267 | value |
| VALUEATOL | 443F:0000 | 443F | value |
| ANSILSTRNCMPI | 2A8F:00D3 | 2A8F | string compare |
| ?SENDPROC@TBXBOBJ@@... | 29AF:0000 | 29AF | ActiveX/OLE |
| VALUENEWTIME | 449F:01C0 | 449F | value |

### Selector groups this batch

- **4457**: VALUETOSTRING, VALUENEW, VALUEAS, VALUEASEX, VALUEASC, VALUEASCEX, VALUECONVERTTOC, VALUECONVERTTOCEX, VALUEFROMSTRING (value conversion cluster)
- **4537**: STACKGETSIZE, VALUENEWSTACK, STACKPUSH, STACKPUSHONE, STACKELEMENT, STACKSETELEMENT (stack cluster)
- **0D37**: CDBCHUNKLAST, CDBCHUNKEND, CDBCHUNKFIND (chunk walkers)
- **450F**: HEAPCREATEFRAME, HEAPGETHANDLER, HEAPRELEASEFRAME (heap)
- **4D27**: RESMGRENUM (resource)
- **3397**: CDBLOCKVALUE (same selector as earlier CDBQUERYVALUE family)
- **381F**: CDBSETPLERR
- **4477**: LPSTRTODOUBLE
- **44FF**: VALUECHECK
- **4267**: VALUENEWLAYEREX
- **443F**: VALUEATOL
- **2A8F**: ANSILSTRNCMPI
- **29AF**: ?SENDPROC@TBXBOBJ@@ (ActiveX)
- **449F**: VALUENEWTIME

### Useful vs noise

Most of this batch is value conversion and stack machinery. Not on the book-open or paint path.

**Worth keeping:**
- CDBCHUNKFIND / CDBCHUNKEND / CDBCHUNKLAST (0D37) — chunk walkers. These walk the property/record chunks. Related to the 14 00 00 reader question.
- CDBLOCKVALUE (3397) — same selector as the earlier CDBQUERYVALUE / CDBSENDVALUEEX family. Value locking.
- OBJFILEOPEN (3147) — file open path.
- ?SENDPROC@TBXBOBJ@@ (29AF) — ActiveX/OLE send. Side quest.

**Skip for now:**
- All STACK* (4537) — stack machine.
- All VALUE* convert/as/check (4457, 44FF, 443F, 4267, 449F) — value type conversion.
- HEAP* (450F) — heap frames.
- ANSILSTRNCMPI (2A8F) — string compare.
- RESMGRENUM (4D27) — resource enum.
- LPSTRTODOUBLE (4477) — string to double.
- CDBSETPLERR (381F) — error set.

The chunk walkers (CDBCHUNK*) are the closest thing to a record reader in this batch. They are not the 14 00 00 reader, but they walk the property chunks that sit inside the page records.

## Callers and first instructions (this batch, interesting ones)

### CDBCHUNKFIND (0D37:0146)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov ax,word ptr 12[bp] / sub ax,0001 / sbb cx,cx / not cx
- Callers visible: 4857:0C68 (????), 4857:090B (call near), 3187:0210 (call far), 322F:0577 (cmp ax,268), 322F:0E1E (jmp word)

### CDBCHUNKEND (0D37:0000)
- First: mov ax,347F / enter 0004,00 / push si / push ds / mov ds,ax / mov word ptr -02[bp],0 / cmp word ptr 0C[bp],00 / jne 003E
- Callers visible: 3187:0210 (call far), 0D37:2B77 (????), 0D37:12BC (????), 0D37:247E (????), 0D37:0AE5 (????), 0D37:07FB (????), CDBCHUNKFIND (jb 0x0297)

### CDBCHUNKLAST (0D37:0334)
- First: mov ax,347F / enter 0010,00 / push si / push ds / mov ds,ax / xor ax,ax / mov word ptr -04[bp],ax / mov word ptr -06[bp],ax
- Callers visible: 4857:090B (call near), 4857:0B23 (call dword), 3187:0210 (call far), CDBCHUNKEND (leave)

### CDBLOCKVALUE (3397:02CA)
- First: mov ax,347F / enter 0002,00 / push ds / mov ds,ax / mov al,byte ptr 0B[bp] / shr al,02 / sub ah,ah / sub ax,001A
- Callers visible: 4857:4FF6 (????), 4857:0C68 (call dword), 4857:42B8 (????), 4857:090B (call near), 3187:0210 (call far), 31B7:0073 (call near), 31B7:00F9 (call near)

### OBJFILEOPEN (3147:177C)
- First: mov ax,347F / enter 025A,00 / push di / push si / push ds / mov ds,ax / mov word ptr -04[bp],...
- Callers visible: 322F:3252 (jmp 0x31FC), 3D6F:0416 (call near), 3D6F:0F79 (call near), 3D6F:0E8E (call far), 3247:0219 (call near), 3247:25A7 (call far), OBJGETFILE, OBJFREESEG

### ?SENDPROC@TBXBOBJ@@ (29AF:0000)
- First: mov ax,347F / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / cmp ax,3014 / jne 0014
- Callers visible: ?GETPROC@TBXBOBJ@@, 29AF:033CE, ?SETPROC@TBXBOBJ@@, SENDPROC@TBXBOBJ@@ (self), 29AF:0206D, ?SETPROC@TBXBOBJ@@

### Matching note
For next boot, match these by function name + first instruction bytes (mov ax,347F is the common entry, then the enter size differs). The 347F is this boot's DGROUP. It will change. The enter size and the next instructions are stable.

## Callers and first instructions (batch 2026-10-15 18:16, interesting ones)

### CDBCLASSTABLEGETBEHAVIOR (44F7:121A)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / cmp word ptr 08[bp],00 / je 129A
- Callers visible: 3197:08A3, 3197:0C3F, 3197:105C, 3CC7:0379, 44F7:026A, 44F7:3FEF
- Note: Unbreaking this let the splash page run. Hit during book open / class-table setup.

### CDBVALUENEWBOOKREF (4267:0000)
- First: mov ax,347F / enter 0004,00 / push ds / mov ds,ax / mov ax,word ptr 08[bp] / or ax,word ptr 06[bp]
- Callers visible: 3467:19AD, 3467:1333, 3467:0B0F, 322F:0E1E, 322F:180D

### VALUENEWGRAPHIC (4267:1494)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov al,byte ptr 11[bp] / and al,FC
- Callers visible: 3467:1934, 3467:1176, 3467:0B0F, 322F:0E1E, 0DC7:1C82, 516F:044B

### VALUENEWBOOK (4267:0D90)
- First: mov ax,347F / enter 0006,00 / push ds / mov ds,ax / mov word ptr -06[bp],0
- Callers visible: 3D6F:0EDF, 3467:0369, 3467:19AD, 3467:1333, 3467:0B0F, 322F:0E1E

### GETDIBCOLORCOUNT (35D7:053A)
- First: mov ax,347F / enter 0006,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp]
- Callers visible: PATTERNDITHER_8BIT, CREATEDITHEREDHEADER_8BIT, GETDIBSIZE, CREATEDIBMASK (self-cluster)

### HUGEGETDATA (33BF:0D6C)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / mov word ptr -04[bp],0
- Callers visible: 33BF:1140, 33BF:02AB, 33BF:0118, 33BF:2CF2, 33BF:0F64, 33BF:0A64, 33BF:0AAD

### OBJREALLOCNEAR (3147:08D6)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp]
- Callers visible: 322F:170F, 409F:0890, 409F:2241, OBJNEWNEAREX, OBJFILECOPY, OBJGETHDRLONG, OBJFREENEAR

### Matching note
Same as prior batches: mov ax,347F is this boot's DGROUP and will change. Match on enter size and the next 2-3 instructions. CDBCLASSTABLEGETBEHAVIOR is the splash-gate observation for this batch.

## Callers and first instructions (batch 2026-10-15 18:22, interesting ones)

### CDBCREATEINSTANCE (480F:0000)
- First: mov ax,347F / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp]
- Callers visible: 4EDF:0067, 0D67:87A2, 322F:170F, 40A7:167A, 40A7:1628, 3DE7:029B, 315F:0231

### CDBVALUEBOOKFROMSTRING (4267:03F4)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / push word ptr 08[bp]
- Callers visible: 4267:1E8F, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWGRAPHIC

### CDBVALUEGRAPHICFROMSTRING (4267:0AA0)
- First: mov ax,347F / enter 0074,00 / push si / push ds / mov ds,ax / mov word ptr -44[bp],0
- Callers visible: CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK

### CDBVALUELAYERFROMSTRBOOK (4267:05F8)
- First: mov ax,347F / enter 004C,00 / push si / push ds / mov ds,ax / mov word ptr -2C[bp],0
- Callers visible: CDBVALUENEWLAYERREF, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWLAYER
- Note: User goofed on CDBVALUELAYERFROMSTRING; two screenshots of this function.

### CDBVALUERESOURCEFROMSTRING (4267:08B2)
- First: mov ax,347F / enter 004A,00 / push ds / mov ds,ax / mov word ptr -2C[bp],0
- Callers visible: CDBVALUEBOOKTOSTRING, CDBVALUENEWBOOKREF, CDBVALUENEWLAYERREF, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWRESOURCE

### Matching note
Same as prior batches: mov ax,347F is this boot's DGROUP and will change. Match on enter size and the next 2-3 instructions.

## Callers and first instructions (batch 2026-10-15 18:32, app now paging)

### GETDIBSIZE (35D7:05DA)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp]
- Callers visible: 35D7:113E (PATTERNDITHER_8BIT), CREATEDITHEREDHEADER_8BIT, 35D7:5EC2, 35D7:4FE5, 35D7:5134, 35D7:197E

### VALUEARRAYCHKDIMS (4357:03D8)
- First: mov ax,347F / enter 0022,00 / push ds / mov ds,ax / mov al,byte ptr 0B[bp]
- Callers visible: 3467:1333, 3467:0B0F, 322F:0E1E, 4DEF:013B, 4D87:00ED, 516F:52BD, 322F:1689

### VALUENEWRESOURCE (4267:0EFC)
- First: mov ax,347F / enter 000E,00 / push di / push si / push ds / mov ds,ax / cmp word ptr 0A[bp],00
- Callers visible: 4D87:0102, 0ED7:1E5B, 4D87:01C72, 0ED7:1E5B, 4C0F:1C72, 518F:4776, 322F:180D

### RESMGRGETREFCNT (4D27:2838)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp]
- Callers visible: 4D87:0102, 0ED7:1E5B, 4C0F:1C72, 518F:4776, 322F:180D, RESMGRREPLACE

### Status note
After this batch the application is up and paging through the book without re-breaking. Splash gate and early constructors have been passed.

## Callers and first instructions (batch 2026-10-15 18:39, menu break)

### COLORHLSTORGB (44B7:0B84)
- First: mov ax,347F / enter 0034,00 / push di / push si / push ds / mov ds,ax / mov ax,word ptr 08[bp] / or ax,word ptr 06[bp] / jne 0BBE / push 0000
- Callers visible: 516F:2ED4, 44B7:1FF7, VALUENEWCOLORTABLE, VALUENEWCOLOR
- Behavior: fired when menu was drawn. Unbreaking returned to the menu. HLS-to-RGB color helper, supporting graphics. Not a gate.

## Callers and first instructions (batch 2026-10-15 18:42, Lesson Exit)

Successful exit. Cleanup paths only.

### CDBUNREGISTERVBXFORM (4437:0068)
- First: mov ax,347F / enter 0002,00 / push ds / mov ds,ax / mov bx,word ptr 08[bp] / mov byte ptr ss:[bx],0 / push bx / push word ptr 06[bp] / push 0001 / call far ptr 4857:02FC
- Callers visible: 3197:03F8, 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX

### VBXDESTROYVIEW (4437:02F0)
- First: mov ax,347F / enter 000E,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp] / mov word ptr -04[bp],bx / mov word ptr -02[bp],es / mov word ptr es:02[bx] / mov ax,word ptr es:06[bx] / or ax,word ptr es:04[bx]
- Callers visible: 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX

### CDBDESTROYINSTANCE (480F:040A)
- First: mov ax,347F / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 08[bp] / push word ptr 06[bp] / push 0003 / call far ptr 4857:02FC
- Callers visible: 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX, 315F:2094, 315F:1194

### Status note
These fire during Lesson Exit. Supporting cleanup (VBX and instance teardown). Not open/render keepers.

## Callers and first instructions (batch 2026-10-15 18:44-18:51, restart)

Segment changed on restart. Object/heap/value init paths. Supporting only.

### HEAPREGISTER (343F:0000)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / cmp word ptr 11AE,0000 / jne 004C / push 2042 / push 0000 / push 002E

### VALUEINIT (44CF:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / les bx,dword ptr 06[bp] / sub ax,ax / mov word ptr es:B0[bx] / mov word ptr es:AE[bx] / mov word ptr es:08[bx]

### VALUENEWARRAY (395F:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 16[bp] / push word ptr 14[bp] / push word ptr 12[bp] / push word ptr 10[bp] / push word ptr 0E[bp]

### TBHEAPALLOC (343F:0840)
- First: mov ax,2977 / enter 0014,00 / push di / push si / push ds / mov ds,ax / mov ax,word ptr 06[bp] / add ax,0004 / cmp ax,word ptr 06[bp] / jae 085A

### HEAPPOINTERTOVALUE (343F:0EE2)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / mov cx,word ptr 06[bp] / mov word ptr -04[bp],cx / mov ax,word ptr 08[bp] / mov es,ax / mov ax,word ptr -02[bp] / mov cx,ax

### CDBINIT (37A7:0000)
- First: mov ax,2977 / enter 00C8,00 / push di / push si / push ds / mov ds,ax / mov bx,word ptr 06[bp] / mov byte ptr ss:[bx],0 / push bx / call far ptr 2A9F:0000

### OBJINIT (4357:0000)
- First: mov ax,2977 / enter 0016,00 / push ds / mov ds,ax / cmp word ptr 034C,0000 / jne 0054 / call far ptr 34F7:0E58 / mov word ptr -08[bp],dx / or dx,ax / je 002D

### VALUENEWSTRING (3397:0000)
- First: mov ax,2977 / enter 0004,00 / push di / push ds / mov ds,ax / cmp word ptr 06[bp],00 / jne 0028 / mov ax,word ptr 0A[bp] / or ax,word ptr 08[bp]

### CDBCREATEINSTANCE (4387:0000)
- First: mov ax,2977 / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp] / mov byte ptr ss:[bx],0 / cmp word ptr 018C,0000 / jne 0028 / mov bx,word ptr 0E[bp]

### CDBREFVALUE (3B6F:0304)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / cmp word ptr 06[bp],00 / jne 0326 / cmp word ptr 08[bp],04 / jne 0326 / mov ax,word ptr 06[bp]

### CDBFILENEW (3B5F:0028)
- First: mov ax,2977 / enter 0022,00 / push ds / mov ds,ax / push word ptr 0E[bp] / push word ptr 0C[bp] / push 0001 / call far ptr 3877:02FC / or ax,ax / jne 0046

### OBJNEWSEG (4867:06E6)
- First: mov ax,2977 / enter 000E,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / mov word ptr 2862,ax / mov word ptr -02[bp],ax

### OBJLOCK (4867:0308)
- First: mov ax,2977 / enter 0006,00 / push ds / mov ds,ax / push word ptr 0C[bp] / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / call far ptr 3AB7:0000 / or ax,ax

### OBJNEWNEAR (4867:0552)
- First: mov ax,2977 / enter 0008,00 / push di / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0C[bp] / mov dx,ax

### LOOKUPSTDPROPBYNAME (337F:010A)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 08[bp] / push word ptr 06[bp] / push word ptr 19FC / push word ptr 19FA / push cs

### OBJTOUCH (4867:0AD4)
- First: mov ax,2977 / enter 0024,00 / push si / push ds / mov ds,ax / mov ax,word ptr 0A[bp] / or ax,word ptr 08[bp] / jne 0AF0 / xor ax,ax / cwd

### OBJOPTOOH (4867:01DA)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / push word ptr 06[bp] / push cs

### OBJOOTOOH (4867:0176)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx / mov es,ax

### OBJNEWNEAREX (4867:0606)
- First: mov ax,2977 / enter 0022,00 / push si / push ds / mov ds,ax / mov bx,word ptr 10[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0E[bp] / sub bx,bx / mov es,ax

### OBJFREENEAREX (4867:0E36)
- First: mov ax,2977 / enter 0016,00 / push si / push ds / mov ds,ax / mov word ptr -04[bp],0 / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx

### SENDPROC@TBXUSER (33DF:0000)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / sub ax,ax / mov word ptr -02[bp],ax / mov word ptr -04[bp],ax / mov ax,word ptr 0E[bp] / sub ax,000A / je 004E

### OBJPRINCIPALOO (4867:0A40)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / push cs / call near ptr OBJPRINCIPALOP

### OBJPRINCIPALOP (4867:0A5C)
- First: mov ax,2977 / enter 0012,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / sub bx,bx / mov es,ax

### SENDPROC@TBXBASE (59DF:0000)
- First: mov ax,2977 / enter 002E,00 / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / cmp ax,3012 / je 0064 / ja 0026 / sub ax,000A / je 0038

### HCACHEPURGE (3787:0690)
- First: mov ax,2977 / enter 0038,00 / push ds / mov ds,ax / cmp word ptr 17E2,0000 / jne 06A4 / jmp near ptr 07EA / mov ax,word ptr 17DC / or ax,word ptr 17DA / jne 06B0

### SETPROC@TBXBASE (59DF:00F4)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / mov bx,word ptr 14[bp] / xor ax,ax / mov byte ptr ss:[bx],7 / cwd / pop ds / leave

### OBJUNLOCK (4867:0432)
- First: mov ax,2977 / enter 004A,00 / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / mov word ptr -4A[bp],ax / sub bx,bx / mov es,ax

### OBJARENACHECK (4397:0AE2)
- First: mov ax,2977 / enter 002A,00 / push ds / mov ds,ax / mov word ptr -02[bp],0 / mov ax,word ptr 14[bp] / sub cx,cx / mov word ptr -06[bp],cx / mov word ptr -04[bp],ax / mov bx,cx

### OBJGETFILE (4867:0094)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / sub bx,bx / mov es,ax

### SENDPROC@TBXLAYER (344F:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / sub ax,302E / je 0048 / sub ax,006A / je 005E

### SETPROC@TBXLAYER (344F:0156)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / sub ax,401B / je 0194 / sub ax,000F / je 01AC

### OBJGETHDRLONG (4867:0242)
- First: mov ax,2977 / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / mov word ptr 2862,ax / mov word ptr -02[bp],ax

### RESMGRSENDMESSAGE (3817:1C82)
- First: mov ax,2977 / enter 0012,00 / push si / push ds / mov ds,ax / sub ax,ax / mov word ptr -10[bp],ax / mov word ptr -12[bp],ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],ax

### CDBCLEARBOOKREFS (3B5F:10A6)
- First: mov ax,2977 / enter 00B8,00 / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / lea ax,-2E[bp] / push ss / push ax / call far ptr 3877:0000

### CDBCREATEBOOKREF (3B5F:0F5C)
- First: mov ax,2977 / enter 000E,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / push bx / push word ptr 0A[bp] / push 0001 / call far ptr 3877:02FC

### CDBGETVALUEEX (3B6F:0D80)
- First: mov ax,2977 / enter 0038,00 / push ds / mov ds,ax / mov word ptr -12[bp],0 / sub ax,ax / mov word ptr -14[bp],ax / mov word ptr -16[bp],ax / mov word ptr -18[bp],ax / mov word ptr -10[bp],0

### OBJLOCKNEAR (4867:03D6)
- First: mov ax,2977 / enter 000E,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx / mov es,ax / mov ax,word ptr es:0000

### CDBVALUENEWGRAPHICREF (33EF:02D4)
- First: mov ax,2977 / enter 0024,00 / push ds / mov ds,ax / lea ax,-02[bp] / push ax / push word ptr 10[bp] / push word ptr 0E[bp] / push word ptr 0C[bp] / push word ptr 0A[bp]

### Status note
Object management, heap, and value creation. Supporting infrastructure for book open. Not open/render keepers. Segment changed on restart.

