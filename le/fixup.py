#
# Copyright (C) 2024-present Mihail Ivanchev
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
import le.const as const
import struct


class FixupRec:
    def __init__(self, data, file_hdr, page_num, offs):

        self._file_hdr = file_hdr
        self._src_page_num = page_num

        rec_offs = file_hdr.hdr_offs + file_hdr.fixup_rec_tbl_offs + offs

        self._src_type = data[rec_offs]
        self._dst_flags = data[rec_offs + 1]

        if self._src_type & const.FSRFC_SOURCE_LIST:
            raise Exception("Fixups with source offset lists are not supported.")
        elif self._src_type != const.FSRCF_32_BIT_OFFS:
            raise Exception("Fixups other than 32-bit offset fixup are not supported.")
        elif self._dst_flags & const.FIXUP_TGT_TYPE_MASK != const.FIXUP_TGT_INTERNAL:
            raise Exception("Only fixups for internal references are supported.")
        elif (self._dst_flags & ~const.FIXUP_TGT_TYPE_MASK) & ~const.FTGTF_32_BIT_OFFS != 0:
            raise Exception("Only fixups for 16-bit or 32-bit target offsets are supported.")

        if self._dst_flags & const.FTGTF_32_BIT_OFFS:
            (self._src_offs, self._dst_obj_num, self._dst_obj_offs) = struct.unpack_from(
                "<hBL", data, rec_offs + 2
            )
            self.rec_size = 9
        else:
            (self._src_offs, self._dst_obj_num, self._dst_obj_offs) = struct.unpack_from(
                "<hBH", data, rec_offs + 2
            )
            self.rec_size = 7

    def __repr__(self):
        dsttype = const.FIXUP_TARGET_TYPE_MAP[self._dst_flags & const.FIXUP_TGT_TYPE_MASK]
        flags = [dsttype]
        for val, name in const.FIXUP_FLAGS_MAP.items():
            if self._dst_flags & val != 0:
                flags.append(name)
        flags = ",".join(flags)
        return (
            "FixupRec("
            f"src_type = {const.FIXUP_SOURCE_MAP[self.src_type]}, "
            f"dst_flags = {flags}, "
            f"src_page_num = {self.src_page_num}, "
            f"src_offs = {self.src_offs}, "
            f"dst_obj_num = {self.dst_obj_num}, "
            f"dst_obj_offs = 0x{self.dst_obj_offs:04X}, "
            f"rec_size = {self.rec_size}, "
            f"label = {self.label})"
        )

    @property
    def file_hdr(self):
        return self._file_hdr

    @property
    def src_page_num(self):
        return self._src_page_num

    @property
    def src_type(self):
        return self._src_type

    @property
    def src_offs(self):
        return self._src_offs

    @property
    def dst_obj_offs(self):
        return self._dst_obj_offs

    @property
    def dst_obj_num(self):
        return self._dst_obj_num

    @property
    def label(self):
        return f"ref_{self.dst_obj_num}_{self.dst_obj_offs:04X}"
