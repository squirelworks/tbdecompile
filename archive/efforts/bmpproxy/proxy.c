/*
 * TB80BMP proxy. A 16-bit NE stand-in that exports ordinals 1..93 and
 * forwards each to the real DLL, renamed TB80BMR.DLL. Ordinals 3
 * (TBKBITMAP) and 13 (TBKGRAPHICFX) are logged to C:\TBK\BMPLOG.TXT.
 *
 * Build with Open Watcom, 16-bit, large model. See build.bat.
 */
#include <windows.h>

/* Real module and the resolved export table. procs[n-1] is ordinal n. */
HINSTANCE       realmod;
void __far      *procs[93];

/* Filled by the logged stubs before they call logfn. */
unsigned        log_ord;
unsigned        log_a;
unsigned        log_b;
void __far      *logfn;

static int      logh = -1;

static void line(char *s, int n)
{
    if (logh != -1)
        _lwrite(logh, s, n);
}

/* Called through logfn by the ordinal 3 and 13 stubs. Reads the globals. */
void __far __pascal logbmp(void)
{
    char    b[96];
    int     n;

    n = wsprintf(b, "ord %u  %04X %04X\r\n", log_ord, log_a, log_b);
    line(b, n);
}

int __far __pascal LibMain(unsigned hInst, unsigned wDS,
                           unsigned cbHeap, unsigned dummy)
{
    char    b[96];
    int     i, n, got;

    logfn = (void __far *)logbmp;

    logh = _lopen("C:\\TBK\\BMPLOG.TXT", OF_READWRITE);
    if (logh == -1)
        logh = _lcreat("C:\\TBK\\BMPLOG.TXT", 0);
    else
        _llseek(logh, 0, 2);

    realmod = LoadLibrary("TB80BMR.DLL");
    got = 0;
    if ((unsigned)realmod >= 32) {
        for (i = 0; i < 93; i++) {
            procs[i] = GetProcAddress(realmod, (LPCSTR)MAKELONG(i + 1, 0));
            if (procs[i] != 0)
                got++;
        }
        n = wsprintf(b, "proxy up  real=%u  resolved=%d/93\r\n", realmod, got);
    } else {
        n = wsprintf(b, "no real TB80BMR  err=%u\r\n", realmod);
    }
    line(b, n);
    return 1;
}

int __far __pascal WEP(int nParam)
{
    if (logh != -1)
        _lclose(logh);
    if ((unsigned)realmod >= 32)
        FreeLibrary(realmod);
    return 1;
}
