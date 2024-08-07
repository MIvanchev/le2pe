#!/bin/python
#
# Copyright (C) 2024-present Mihail Ivanchev
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
import struct
import sys
from io import StringIO
from le import Header, Object, FixupRec
from pathlib import Path


class ByteCache:
    def __init__(self, fp, size=16, ascii=False):
        self.fp = fp
        self.data = [0 for _ in range(size)]
        self.size = 0
        self.ascii = ascii

    def add(self, val):
        if self.size == len(self.data):
            self.emit()

        self.data[self.size] = val
        self.size += 1

    def emit(self):
        if self.size > 0:
            output = StringIO()
            output.write('db `')
            for ii in range(self.size):
                val = self.data[ii]
                if self.ascii and val >= 0x20 and val <= 0x7E:
                    output.write(chr(val))
                else:
                    output.write(f"\\x{self.data[ii]:02X}")
            output.write('`\n')
            fp.write(output.getvalue())
            self.size = 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: le2pe.py <LE file> <ASM file>", file=sys.stderr)
        exit(1)

    data = Path(sys.argv[1]).read_bytes()
    le_offset = struct.unpack_from("<L", data, 0x3C)[0]
    hdr = Header(data, le_offset)

    print(hdr)
    print()

    obj_map = {}
    obj_by_page = {}
    fixups = {}
    label_defs = {}

    print("Object table")
    for ii in range(hdr.num_objects):
        obj = Object(data, hdr, ii + 1)
        obj_map[obj.number] = obj
        for page in obj.pages:
            obj_by_page[page.number] = obj
        print(f"    #{ii+1}: {obj}")

    label_defs[(hdr.eip_obj, hdr.eip)] = "_start"

    # for ii in range(hdr.num_objects):
    #     print()
    #     print(f"Pages for object {ii + 1}")
    #     for page in obj_map[ii + 1].pages:
    #         print(f"    {page}")

    for ii in range(hdr.num_pages):
        (fixup_off, fixup_off_next) = struct.unpack_from(
            "<LL", data, hdr.hdr_offs + hdr.fixup_page_tbl_offs + ii * 4
        )

        while fixup_off != fixup_off_next:
            fixup = FixupRec(data, hdr, ii + 1, fixup_off)

            if fixup.src_offs >= 0:
                obj_by_page[fixup.src_page_num].add_fixup(fixup)
                label_defs[(fixup.dst_obj_num, fixup.dst_obj_offs)] = fixup.label
                # print(f"        {fixup}")

            fixup_off += fixup.rec_size

    with Path(sys.argv[2]).open("w", encoding="utf-8") as fp:
        fp.write("global _start\n")

        for obj_num, obj in obj_map.items():
            fp.write("\n")
            if obj.is_executable:
                fp.write("section .text\n\n")
            else:
                fp.write("section .data\n\n")

            cache = ByteCache(fp, ascii=False)

            # TODO: For some reason there is less data in the file than
            # required for the data segment's pages, let's work around
            # this issue until we find the cause.

            idx = 0
            while idx < obj.size:
                label_def = label_defs.get((obj_num, idx))
                if label_def:
                    cache.emit()
                    fp.write(f"{label_def}:\n")

                fixup = obj.get_fixup(idx)

                if fixup:
                    cache.emit()
                    fp.write(f"dd {fixup.label}\n")
                    idx += 4
                else:
                    cache.add(data[obj.data_offs + idx])
                    idx += 1

            cache.emit()

            num_bytes = 0
            while idx < obj.virtual_size:
                label_def = label_defs.get((obj_num, idx))
                if label_def:
                    fp.write(f"resb {num_bytes}\n")
                    fp.write(f"{label_def}:\n")
                    num_bytes = 0

                idx += 1
                num_bytes += 1

            if num_bytes > 0:
                fp.write(f"resb {num_bytes}\n")
