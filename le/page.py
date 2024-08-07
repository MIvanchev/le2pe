#
# Copyright (C) 2024-present Mihail Ivanchev
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
import le.const as const
import struct


class PageInfo:
    def __init__(self, data, file_hdr, number):
        self._file_hdr = file_hdr

        offs = file_hdr.hdr_offs + file_hdr.obj_page_tbl_offs + (
                    number - 1
                ) * 4

        num3, num2, num1, self._flags = struct.unpack_from(
            "4B", data, offs
        )

        self._number = num1 | (num2 << 8) | (num3 << 16)

        assert number == self._number

        if self._flags != const.PAGE_VALID:
            raise Exception('Pages with flags other than PAGE_VALID are not supported.')

        if self.number == file_hdr.num_pages:
            self._size = file_hdr.last_page_size
        else:
            self._size = file_hdr.page_size

    def __repr__(self):
        return (
            "PageMapEntry("
            f"number = {self.number}, "
            f"flags = {const.PAGE_FLAGS_MAP[self.flags]}, "
            f"size = {self.size})"
        )

    @property
    def file_hdr(self):
        return self._file_hdr

    @property
    def number(self):
        return self._number

    @property
    def flags(self):
        return self._flags

    @property
    def size(self):
        return self._size
