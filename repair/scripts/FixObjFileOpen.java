// Rebuilds OBJFILEOPEN as one function, 1170:177c through 1170:21f1.
// See repair/01-call-return-split.md. The public class name matches this file.
//@category Toolbook

import java.util.ArrayList;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.FlowOverride;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.symbol.SourceType;

public class FixObjFileOpen extends GhidraScript {

    @Override
    public void run() throws Exception {
        Address start = toAddr("1170:177c");
        Address end = toAddr("1170:21f1");
        AddressSet span = new AddressSet(start, end);
        Listing listing = currentProgram.getListing();
        FunctionManager functions = currentProgram.getFunctionManager();

        Function callee = functions.getFunctionAt(toAddr("1160:0774"));
        if (callee != null && callee.hasNoReturn()) {
            callee.setNoReturn(false);
        }

        Instruction inst = listing.getInstructionAt(start);
        while (inst != null && inst.getAddress().compareTo(end) <= 0) {
            if (inst.getFlowOverride() != FlowOverride.NONE) {
                inst.setFlowOverride(FlowOverride.NONE);
            }
            inst = inst.getNext();
        }

        ArrayList<Function> cut = new ArrayList<>();
        FunctionIterator it = functions.getFunctions(span, true);
        while (it.hasNext()) {
            cut.add(it.next());
        }
        for (Function fn : cut) {
            removeFunction(fn);
        }

        disassemble(start);
        functions.createFunction("OBJFILEOPEN", start, span, SourceType.USER_DEFINED);
    }
}
