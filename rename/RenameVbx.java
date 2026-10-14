// Rename TB80VBX functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80VBX functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameVbx extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1008_12b2", "VbxCreateWindow"},
        {"FUN_1020_13fe", "VbxBitBlt"},
        {"FUN_1038_1bd8", "VbxAlloc"},
        {"FUN_1058_0534", "VbxAlloc2"},
        {"FUN_1058_0910", "VbxBitBlt2"},
        {"FUN_1058_0ac6", "VbxAlloc3"}
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
