## le2pe
Converter for DOS LE executables to the Portable Executable (PE) format

The main use case for this converter is to broaden the set of available tools
for the executable file's analysis, since PE files are widely supported. The
converted result should be executable through
[HX DOS](https://github.com/Baron-von-Riedesel/HX).

### Usage

This software is written in Python, to run execute

```
./le2py.py <LE file> <ASM file>
```

The output is an NASM-usable assembler file containing the sections of the LE
program with label references for the sources and targets of fixups
(relocations). `dd <relocation-target>` is placed at the source of a fixup and
`<relocation-target>:` is placed at the target. Thus, the linker can
automatically generate relocation info. Only a very limited set of fixups is
supported for now. The entry point of the program is labeled `_start`.
You can link with LD through

```
nasm -w-zeroing -f win32 <ASM file> && ld -mi386pe -e _start -o <PE file>
```

Use at your own risk and discretion. I assume no responsibility for any damage
resulting from using this project.

### Credits

Initial idea by Grom PE https://board.flatassembler.net/topic.php?t=19893

Useful resources on the LE format:
* https://github.com/open-watcom/open-watcom-v2/blob/master/bld/watcom/h/exeflat.h
* https://fd.lod.bz/rbil/interrup/dos_kernel/214b.html#table-01610
* http://www.textfiles.com/programming/FORMATS/lxexe.txt
* https://github.com/yetmorecode/ghidra-lx-loader/blob/master/src/main/java/yetmorecode/ghidra/format/lx/model/Header.java
* https://gist.github.com/gsuberland/117433f2b4c12e83e0207ad41c9eeedc

