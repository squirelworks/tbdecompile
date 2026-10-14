# Rename the TB80W16 functions we have pinned down.
# Run from Ghidra Script Manager against the TB80W16 project.

#@category ToolBook
#@menupath ToolBook.Rename W16 functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Memory
    ("FUN_1010_1914", "W16Alloc"),
    ("FUN_1058_0f14", "W16Lock"),
    ("FUN_1058_2568", "W16Alloc2"),
    ("FUN_10b0_0060", "W16Lock2"),
    # String
    ("FUN_1030_003a", "W16StrCpy"),
    ("FUN_10b0_022c", "W16StrLen"),
    ("FUN_10c0_013a", "W16StrCat"),
    ("FUN_10c0_0310", "W16StrHelper"),
]

println("program: %s" % currentProgram.getName())
renamed = 0
for old, new in RENAMES:
    hits = getGlobalFunctions(old)
    if hits is None or len(hits) == 0:
        println("NOT FOUND: %s" % old)
        continue
    for func in hits:
        func.setName(new, SourceType.USER_DEFINED)
        println("renamed %s -> %s at %s" % (old, new, func.getEntryPoint()))
        renamed += 1
println("done, renamed %d" % renamed)
