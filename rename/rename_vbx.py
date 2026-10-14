# Rename the TB80VBX functions we have pinned down.
# Run from Ghidra Script Manager against the TB80VBX project.

#@category ToolBook
#@menupath ToolBook.Rename VBX functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Window / GDI / Memory
    ("FUN_1008_12b2", "VbxCreateWindow"),
    ("FUN_1020_13fe", "VbxBitBlt"),
    ("FUN_1038_1bd8", "VbxAlloc"),
    ("FUN_1058_0534", "VbxAlloc2"),
    ("FUN_1058_0910", "VbxBitBlt2"),
    ("FUN_1058_0ac6", "VbxAlloc3"),
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
