// Rename TB80RCR functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80RCR functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameRcr extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1008_158c", "RcrBitBlt"},
        {"FUN_1008_164c", "RcrBitBlt2"},
        {"FUN_1008_170e", "RcrBitBlt3"},
        {"FUN_1008_077a", "RcrSendMessage"},
        {"FUN_1008_0e94", "RcrSendMessage2"},
        {"FUN_1008_11aa", "RcrSendMessage3"},
        {"FUN_1008_08e2", "RcrAlloc"},
        {"FUN_1008_2190", "RcrAlloc2"},
        {"FUN_1008_aa62", "RcrStrCpy"}
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
