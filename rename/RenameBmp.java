// Rename TB80BMP functions. Run from Ghidra Script Manager.
//@category ToolBook
//@menupath ToolBook.Rename TB80BMP functions

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import java.util.List;

public class RenameBmp extends GhidraScript {

    private static final String[][] RENAMES = {
        {"FUN_1078_05c2", "CreateDibBitmap"},
        {"FUN_1090_0558", "CreateDibBitmapAlt"},
        {"FUN_1098_0874", "CreateDibBitmapAlt2"},
        {"FUN_10a0_16ee", "CreateDibBitmapAlt3"},
        {"FUN_1048_0116", "BitBltBmp"},
        {"FUN_1048_1250", "BitBltBmp2"},
        {"FUN_1048_2c5e", "BitBltBmp3"},
        {"FUN_1080_0194", "BitBltBmp4"},
        {"FUN_1010_18a4", "SelectPaletteBmp"},
        {"FUN_1030_03e4", "GetDcBmp"},
        {"FUN_1080_0548", "SelectPaletteBmp2"},
        {"FUN_1000_0031", "Lz77Expand"},
        {"FUN_1000_0162", "Lz77ExpandCaller"},
        {"FUN_1000_0752", "Lz77ExpandCaller2"}
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
