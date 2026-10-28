@echo off
rem Open Watcom 16-bit build for the TB80BMP proxy.
rem Forces the 16-bit Windows headers and libs, not the NT ones.

set INCLUDE=C:\WATCOM\H;C:\WATCOM\H\WIN
set LIB=C:\WATCOM\LIB286;C:\WATCOM\LIB286\WIN

wcc -ml -bd -zu -s -zl -zq -3 -bt=windows proxy.c
if errorlevel 1 goto fail
wasm -zq -ml stubs.asm
if errorlevel 1 goto fail
wlink system windows dll initinstance option map file proxy,stubs library windows,kernel name proxy
if errorlevel 1 goto fail
echo built proxy.dll
goto end
:fail
echo build failed
:end
