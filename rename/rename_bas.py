# Rename the TB80BAS functions we have pinned down.
# Run from Ghidra Script Manager against the TB80BAS project.

#@category ToolBook
#@menupath ToolBook.Rename BAS functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Paint
    ("FUN_1408_0376", "CDBPAINTPOLYGON"),
    ("FUN_13e8_00e6", "CDBPAINTPOLYLINE"),
    ("FUN_10a0_0558", "CDBPAINTARC"),
    ("FUN_10a0_0458", "CDBPAINTARCALT"),
    ("FUN_1020_03e4", "CDBPAINTRECTANGLE"),
    # Scale / property
    ("FUN_1008_01dd", "CDBSCALETWIPSTOSCREEN"),
    ("FUN_12d0_03ec", "CDBSETPROPERTY"),
    ("FUN_1408_00d8", "CDBSETPOINTARRAY"),
    ("FUN_12d0_086c", "CDBSETUPPAINTRECT"),
    ("FUN_1008_03f6", "CDBSETSCRIPTPROPERTY"),
    ("FUN_1070_1774", "CDBVALIDATEPROPERTY"),
    ("FUN_1070_1b3c", "CDBCHECKVERTICES"),

    # Additional paint
    ("FUN_1230_2f1c", "CDBPAINTELLIPSE"),
    ("FUN_13d8_0066", "CDBPAINTELLIPSEALT"),
    ("FUN_1230_2278", "CDBPAINTROUNDRECT"),
    ("FUN_1230_26f4", "CDBPAINTROUNDRECTALT"),
    ("FUN_13e0_015a", "CDBPAINTROUNDRECTALT2"),
    ("FUN_1230_2b5a", "CDBPAINTARC2"),
    # Additional property
    ("FUN_10e0_208e", "CDBSETMULTIPROPERTY"),
    ("FUN_10e8_33e8", "CDBSETMULTIPROPERTY2"),
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
