// Rename TB80UTL functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80UTL functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameUtl extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1000_093b", "UtlAlloc"},
        {"FUN_1018_1472", "UtlLock"},
        {"FUN_10b8_0eac", "UtlAlloc2"},
        {"FUN_10c0_028c", "UtlLock2"},
        {"FUN_1008_0504", "UtlStrCpy"},
        {"FUN_10b8_0000", "UtlStrLen"},
        {"FUN_10c8_001e", "UtlStrCat"}
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
