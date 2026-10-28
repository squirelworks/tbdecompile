# FUN_1028_2680 is a filter registrar, not the record reader

> Trail, 2026-10-16. Chapter 4. Closed. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: user-pasted decompile of FUN_1028_2680

## What it actually does

```c
puVar7 = (uint *)TBREGISTERFILTER();
if (puVar7 != (uint *)0x0) {
  local_28 = 0;
  if (*puVar7 != 0) {
    local_30 = (uint *)CONCAT22(((uint *)puVar7)[2],(uint *)(((uint *)puVar7)[1] + 2));
    do {
      if (*local_30 < 0x14) {
        iVar3 = *local_30 * 4;
        *(undefined2 *)(iVar3 + 0x154) = puVar2 + -1;
        *(undefined2 *)(iVar3 + 0x156) = uVar4;
        // ... fill a local struct ...
        (**(code **)(puVar2 + 1))(uVar5,local_1e);   // call the filter's function pointer
      }
      local_30 = (uint *)CONCAT22(uVar4,puVar2 + 0x234);
      local_28 = local_28 + 1;
    } while (local_28 < *puVar7);
  }
}
```

- Calls `TBREGISTERFILTER()` to get a table.
- Walks entries. Each entry starts with a word.
- If that word is `< 0x14`, treats it as a type index, stores a pointer at `type*4 + 0x154`, and calls the function pointer at `puVar2 + 1`.
- The `0x14` is a type-code limit, not the record signature `14 00 00`.

Incoming reference is only `FUN_1028_2648`. Outgoing is `TBREGISTERFILTER`.

## Why the earlier note flagged it

The assembly-pattern search looked for `CMP AX, 0x14` after a word read from a far pointer. This function has that pattern, but the comparison is against a filter type code, not against the three-byte record marker.

## Caller: FUN_1028_2648

```c
void FUN_1028_2648(int param_1,undefined2 param_2)
{
  if (*(int *)(param_1 * 4 + 0x156) == 0 && *(int *)(param_1 * 4 + 0x154) == 0) {
    FUN_1028_2680(0,0,param_1,param_2);
    return;
  }
  return;
}
```

Lazy fill: if the slot for `param_1` is still null, call the registrar; otherwise return.

Incoming references to `FUN_1028_2648`:
- `RESMGRQUERYINFO`
- `RESMGRCHOOSEFILE`
- `FUN_1028_32c8`

These are resource-manager entries (query info, choose file). The filter table is for resource/file types, not for walking `14 00 00` page records.

## Status

`FUN_1028_2680` / `FUN_1028_2648` is a resource-manager filter registrar. Not the page-record reader. Candidate closed.
