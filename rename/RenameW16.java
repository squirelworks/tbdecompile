// Rename TB80W16 functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80W16 functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameW16 extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1010_1914", "W16Alloc"},
        {"FUN_1058_0f14", "W16Lock"},
        {"FUN_1058_2568", "W16Alloc2"},
        {"FUN_10b0_0060", "W16Lock2"},
        {"FUN_1030_003a", "W16StrCpy"},
        {"FUN_10b0_022c", "W16StrLen"},
        {"FUN_10c0_013a", "W16StrCat"},
        {"FUN_10c0_0310", "W16StrHelper"}
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
