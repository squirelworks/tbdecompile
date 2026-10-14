// Rename the TB80BAS functions we have pinned down.
// Run from Ghidra Script Manager against the TB80BAS project.
//@category ToolBook
//@menupath ToolBook.Rename BAS functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;

import java.util.List;

public class RenameBas extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1408_0376", "CDBPAINTPOLYGON"},
        {"FUN_13e8_00e6", "CDBPAINTPOLYLINE"},
        {"FUN_10a0_0558", "CDBPAINTARC"},
        {"FUN_10a0_0458", "CDBPAINTARCALT"},
        {"FUN_1020_03e4", "CDBPAINTRECTANGLE"},
        {"FUN_1008_01dd", "CDBSCALETWIPSTOSCREEN"},
        {"FUN_12d0_03ec", "CDBSETPROPERTY"},
        {"FUN_1408_00d8", "CDBSETPOINTARRAY"},
        {"FUN_12d0_086c", "CDBSETUPPAINTRECT"},
        {"FUN_1008_03f6", "CDBSETSCRIPTPROPERTY"},
        {"FUN_1070_1774", "CDBVALIDATEPROPERTY"},
        {"FUN_1070_1b3c", "CDBCHECKVERTICES"},
        {"FUN_1230_2f1c", "CDBPAINTELLIPSE"},
        {"FUN_13d8_0066", "CDBPAINTELLIPSEALT"},
        {"FUN_1230_2278", "CDBPAINTROUNDRECT"},
        {"FUN_1230_26f4", "CDBPAINTROUNDRECTALT"},
        {"FUN_13e0_015a", "CDBPAINTROUNDRECTALT2"},
        {"FUN_1230_2b5a", "CDBPAINTARC2"},
        {"FUN_10e0_208e", "CDBSETMULTIPROPERTY"},
        {"FUN_10e8_33e8", "CDBSETMULTIPROPERTY2"},
    };

    @Override
    public void run() throws Exception {
        println("program: " + currentProgram.getName());
        int renamed = 0;
        for (String[] pair : RENAMES) {
            String oldName = pair[0];
            String newName = pair[1];
            List<Function> hits = getGlobalFunctions(oldName);
            if (hits == null || hits.isEmpty()) {
                println("NOT FOUND: " + oldName);
                continue;
            }
            for (Function func : hits) {
                func.setName(newName, SourceType.USER_DEFINED);
                println("renamed " + oldName + " -> " + newName + " at " + func.getEntryPoint());
                renamed++;
            }
        }
        println("done, renamed " + renamed);
    }
}
