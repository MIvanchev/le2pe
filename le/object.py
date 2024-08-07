#
# Copyright (C) 2024-present Mihail Ivanchev
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
import le.const as const
import le.page as page
import struct


class Object:
    def __init__(self, data, file_hdr, number):
        self._file_hdr = file_hdr
        self._number = number

        (
            self._virtual_size,
            self._reloc_base_addr,
            self._flags,
            first_page_num,
            num_pages,
        ) = struct.unpack_from("<5L", data, file_hdr.hdr_offs + file_hdr.obj_tbl_offs + (number - 1) * 24)

        self._pages = []
        self._fixups = {}

        for page_num in range(first_page_num, first_page_num + num_pages):
            self._pages.append(page.PageInfo(data, file_hdr, page_num))

    def __repr__(self):
        objtype = const.OBJECT_TYPE_MAP[self.flags & const.OBJ_TYPE_MASK]
        flags = [objtype]
        for val, name in const.OBJECT_FLAGS_MAP.items():
            if self.flags & val != 0:
                flags.append(name)
        flags = ",".join(flags)
        return (f"Object("
                f"flags = {flags}, "
                f"size = 0x{self.size:04X}, "
                f"virtual_size = 0x{self.virtual_size:04X}, "
                f"reloc_base_addr = 0x{self.reloc_base_addr:04X}, "
                f"pages = {self.pages[0].number}-{self.pages[-1].number}, "
                f"data_offs = 0x{self.data_offs:04X})")

    def add_fixup(self, fixup):
        self._fixups[(fixup.src_page_num - self.pages[0].number) * self.file_hdr.page_size + fixup.src_offs] = fixup

    def get_fixup(self, data_offs):
        return self._fixups.get(data_offs)

    @property
    def file_hdr(self):
        return self._file_hdr

    @property
    def is_executable(self):
        return self.flags & const.OBJF_EXECUTABLE

    @property
    def number(self):
        return self._number

    @property
    def flags(self):
        return self._flags

    @property
    def size(self):
        return sum([page.size for page in self.pages])

    @property
    def virtual_size(self):
        return self._virtual_size

    @property
    def reloc_base_addr(self):
        return self._reloc_base_addr

    @property
    def pages(self):
        return self._pages

    @property
    def data_offs(self):
        return self.file_hdr.page_data_offs \
                + (self.pages[0].number - 1) * self.file_hdr.page_size
