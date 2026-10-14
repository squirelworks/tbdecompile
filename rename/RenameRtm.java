// Rename TB80RTM functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80RTM functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameRtm extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_10e0_0050", "PaintRectangle"},
        {"FUN_1398_05c6", "PaintRectangleAlt"},
        {"FUN_1070_0b32", "BitBltHelper"},
        {"FUN_10d0_2d4e", "BitBltHelper2"},
        {"FUN_10d0_2fa0", "BitBltHelper3"},
        {"FUN_10e0_0dea", "BitBltHelper4"},
        {"FUN_1130_32ce", "BitBltHelper5"},
        {"FUN_1010_1a0a", "SendMessageHelper"}
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
