// Rename TB80MM functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80MM functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameMm extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1070_03f4", "MmSendMessage"},
        {"FUN_1088_0200", "MmSendMessage2"},
        {"FUN_1088_0642", "MmSendMessage3"},
        {"FUN_1088_09f0", "MmCreateWindow"},
        {"FUN_1048_00d0", "MmAlloc"},
        {"FUN_1098_006a", "MmAllocStr"},
        {"FUN_1098_0134", "MmStrCpy"}
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
