; 16-bit forwarding stubs. wasm-friendly: no sp indexing, no macro math.
.286
                PUBLIC  E1,E2,E3,E4,E5,E6,E7,E8,E9
                PUBLIC  E10,E11,E12,E13,E14,E15,E16,E17,E18,E19
                PUBLIC  E20,E21,E22,E23,E24,E25,E26,E27,E28,E29
                PUBLIC  E30,E31,E32,E33,E34,E35,E36,E37,E38,E39
                PUBLIC  E40,E41,E42,E43,E44,E45,E46,E47,E48,E49
                PUBLIC  E50,E51,E52,E53,E54,E55,E56,E57,E58,E59
                PUBLIC  E60,E61,E62,E63,E64,E65,E66,E67,E68,E69
                PUBLIC  E70,E71,E72,E73,E74,E75,E76,E77,E78,E79
                PUBLIC  E80,E81,E82,E83,E84,E85,E86,E87,E88,E89
                PUBLIC  E90,E91,E92,E93
                EXTRN   _procs:DWORD
                EXTRN   _logfn:DWORD
                EXTRN   _log_ord:WORD
                EXTRN   _log_a:WORD
                EXTRN   _log_b:WORD

_TEXT           SEGMENT WORD PUBLIC 'CODE'
                ASSUME  CS:_TEXT

E1:
                mov     bx, 0
                jmp     dword ptr _procs[bx]

E2:
                mov     bx, 4
                jmp     dword ptr _procs[bx]

E3:
                mov     bx, sp
                mov     ax, ss:[bx+4]
                mov     word ptr _log_a, ax
                mov     ax, ss:[bx+6]
                mov     word ptr _log_b, ax
                mov     ax, 3
                mov     word ptr _log_ord, ax
                call    dword ptr _logfn
                mov     bx, 8
                jmp     dword ptr _procs[bx]

E4:
                mov     bx, 12
                jmp     dword ptr _procs[bx]

E5:
                mov     bx, 16
                jmp     dword ptr _procs[bx]

E6:
                mov     bx, 20
                jmp     dword ptr _procs[bx]

E7:
                mov     bx, 24
                jmp     dword ptr _procs[bx]

E8:
                mov     bx, 28
                jmp     dword ptr _procs[bx]

E9:
                mov     bx, 32
                jmp     dword ptr _procs[bx]

E10:
                mov     bx, 36
                jmp     dword ptr _procs[bx]

E11:
                mov     bx, 40
                jmp     dword ptr _procs[bx]

E12:
                mov     bx, 44
                jmp     dword ptr _procs[bx]

E13:
                mov     bx, sp
                mov     ax, ss:[bx+4]
                mov     word ptr _log_a, ax
                mov     ax, ss:[bx+6]
                mov     word ptr _log_b, ax
                mov     ax, 13
                mov     word ptr _log_ord, ax
                call    dword ptr _logfn
                mov     bx, 48
                jmp     dword ptr _procs[bx]

E14:
                mov     bx, 52
                jmp     dword ptr _procs[bx]

E15:
                mov     bx, 56
                jmp     dword ptr _procs[bx]

E16:
                mov     bx, 60
                jmp     dword ptr _procs[bx]

E17:
                mov     bx, 64
                jmp     dword ptr _procs[bx]

E18:
                mov     bx, 68
                jmp     dword ptr _procs[bx]

E19:
                mov     bx, 72
                jmp     dword ptr _procs[bx]

E20:
                mov     bx, 76
                jmp     dword ptr _procs[bx]

E21:
                mov     bx, 80
                jmp     dword ptr _procs[bx]

E22:
                mov     bx, 84
                jmp     dword ptr _procs[bx]

E23:
                mov     bx, 88
                jmp     dword ptr _procs[bx]

E24:
                mov     bx, 92
                jmp     dword ptr _procs[bx]

E25:
                mov     bx, 96
                jmp     dword ptr _procs[bx]

E26:
                mov     bx, 100
                jmp     dword ptr _procs[bx]

E27:
                mov     bx, 104
                jmp     dword ptr _procs[bx]

E28:
                mov     bx, 108
                jmp     dword ptr _procs[bx]

E29:
                mov     bx, 112
                jmp     dword ptr _procs[bx]

E30:
                mov     bx, 116
                jmp     dword ptr _procs[bx]

E31:
                mov     bx, 120
                jmp     dword ptr _procs[bx]

E32:
                mov     bx, 124
                jmp     dword ptr _procs[bx]

E33:
                mov     bx, 128
                jmp     dword ptr _procs[bx]

E34:
                mov     bx, 132
                jmp     dword ptr _procs[bx]

E35:
                mov     bx, 136
                jmp     dword ptr _procs[bx]

E36:
                mov     bx, 140
                jmp     dword ptr _procs[bx]

E37:
                mov     bx, 144
                jmp     dword ptr _procs[bx]

E38:
                mov     bx, 148
                jmp     dword ptr _procs[bx]

E39:
                mov     bx, 152
                jmp     dword ptr _procs[bx]

E40:
                mov     bx, 156
                jmp     dword ptr _procs[bx]

E41:
                mov     bx, 160
                jmp     dword ptr _procs[bx]

E42:
                mov     bx, 164
                jmp     dword ptr _procs[bx]

E43:
                mov     bx, 168
                jmp     dword ptr _procs[bx]

E44:
                mov     bx, 172
                jmp     dword ptr _procs[bx]

E45:
                mov     bx, 176
                jmp     dword ptr _procs[bx]

E46:
                mov     bx, 180
                jmp     dword ptr _procs[bx]

E47:
                mov     bx, 184
                jmp     dword ptr _procs[bx]

E48:
                mov     bx, 188
                jmp     dword ptr _procs[bx]

E49:
                mov     bx, 192
                jmp     dword ptr _procs[bx]

E50:
                mov     bx, 196
                jmp     dword ptr _procs[bx]

E51:
                mov     bx, 200
                jmp     dword ptr _procs[bx]

E52:
                mov     bx, 204
                jmp     dword ptr _procs[bx]

E53:
                mov     bx, 208
                jmp     dword ptr _procs[bx]

E54:
                mov     bx, 212
                jmp     dword ptr _procs[bx]

E55:
                mov     bx, 216
                jmp     dword ptr _procs[bx]

E56:
                mov     bx, 220
                jmp     dword ptr _procs[bx]

E57:
                mov     bx, 224
                jmp     dword ptr _procs[bx]

E58:
                mov     bx, 228
                jmp     dword ptr _procs[bx]

E59:
                mov     bx, 232
                jmp     dword ptr _procs[bx]

E60:
                mov     bx, 236
                jmp     dword ptr _procs[bx]

E61:
                mov     bx, 240
                jmp     dword ptr _procs[bx]

E62:
                mov     bx, 244
                jmp     dword ptr _procs[bx]

E63:
                mov     bx, 248
                jmp     dword ptr _procs[bx]

E64:
                mov     bx, 252
                jmp     dword ptr _procs[bx]

E65:
                mov     bx, 256
                jmp     dword ptr _procs[bx]

E66:
                mov     bx, 260
                jmp     dword ptr _procs[bx]

E67:
                mov     bx, 264
                jmp     dword ptr _procs[bx]

E68:
                mov     bx, 268
                jmp     dword ptr _procs[bx]

E69:
                mov     bx, 272
                jmp     dword ptr _procs[bx]

E70:
                mov     bx, 276
                jmp     dword ptr _procs[bx]

E71:
                mov     bx, 280
                jmp     dword ptr _procs[bx]

E72:
                mov     bx, 284
                jmp     dword ptr _procs[bx]

E73:
                mov     bx, 288
                jmp     dword ptr _procs[bx]

E74:
                mov     bx, 292
                jmp     dword ptr _procs[bx]

E75:
                mov     bx, 296
                jmp     dword ptr _procs[bx]

E76:
                mov     bx, 300
                jmp     dword ptr _procs[bx]

E77:
                mov     bx, 304
                jmp     dword ptr _procs[bx]

E78:
                mov     bx, 308
                jmp     dword ptr _procs[bx]

E79:
                mov     bx, 312
                jmp     dword ptr _procs[bx]

E80:
                mov     bx, 316
                jmp     dword ptr _procs[bx]

E81:
                mov     bx, 320
                jmp     dword ptr _procs[bx]

E82:
                mov     bx, 324
                jmp     dword ptr _procs[bx]

E83:
                mov     bx, 328
                jmp     dword ptr _procs[bx]

E84:
                mov     bx, 332
                jmp     dword ptr _procs[bx]

E85:
                mov     bx, 336
                jmp     dword ptr _procs[bx]

E86:
                mov     bx, 340
                jmp     dword ptr _procs[bx]

E87:
                mov     bx, 344
                jmp     dword ptr _procs[bx]

E88:
                mov     bx, 348
                jmp     dword ptr _procs[bx]

E89:
                mov     bx, 352
                jmp     dword ptr _procs[bx]

E90:
                mov     bx, 356
                jmp     dword ptr _procs[bx]

E91:
                mov     bx, 360
                jmp     dword ptr _procs[bx]

E92:
                mov     bx, 364
                jmp     dword ptr _procs[bx]

E93:
                mov     bx, 368
                jmp     dword ptr _procs[bx]

_TEXT           ENDS
                END
