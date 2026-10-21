# Class table

Every book carries its own class registry. It is the class `0x3A` record, `ClassTbl`: a list of `0x2C`-byte rows. A row holds the class number, its parent, and its name.

`0x3A` is that table. It is not the first extension class. In the sample books the next free class number is `0x3D`.

Class `0x26` is `Viewer`. The label `OLEDispatch` for that number is wrong.

Class extra bytes are stored once on the class, not on each object.
