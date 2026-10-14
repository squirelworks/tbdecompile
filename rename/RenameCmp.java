// Rename TB80CMP functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80CMP functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameCmp extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1010_0ee6", "LoadCompilerResource"},
        {"FUN_1010_1390", "LockCompilerResource"},
        {"FUN_1038_0dea", "LockCompilerResource2"},
        {"FUN_1040_0970", "ExpandTextCore"},
        {"FUN_1010_0070", "CompilerStrLen"},
        {"FUN_1010_1774", "CompilerStrCpy"},
        {"FUN_1010_1a28", "CompilerStrCat"},
        {"FUN_1038_06f8", "CompilerStrHelper"}
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
