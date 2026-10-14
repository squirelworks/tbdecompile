// Rename TB80NET functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80NET functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameNet extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1038_01b4", "NetSendMessage"},
        {"FUN_1038_0484", "NetSendMessage2"},
        {"FUN_1040_0000", "NetSendMessage3"},
        {"FUN_1008_17c8", "NetCreateWindow"},
        {"FUN_1008_0862", "NetAlloc"},
        {"FUN_1008_136c", "NetAlloc2"},
        {"FUN_1020_0410", "NetStrCpy"},
        {"FUN_1020_0a10", "NetStrCpy2"}
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
