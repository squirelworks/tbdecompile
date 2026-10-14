// Rename TB80LNL functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80LNL functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameLnl extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1018_04a6", "LnlAlloc"},
        {"FUN_1050_043a", "LnlLock"},
        {"FUN_1070_203e", "LnlAlloc2"},
        {"FUN_10d8_097e", "LnlLock2"},
        {"FUN_1040_344c", "LnlStrCpy"},
        {"FUN_1040_40f0", "LnlStrLen"},
        {"FUN_1090_0130", "LnlStrCat"}
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
