import le.const as const
import struct


class Header:
    def __init__(self, data, hdr_offs):
        self._hdr_offs = hdr_offs

        (
            self._signature,
            self._byte_order,
            self._word_order,
            self._level,
            self._cpu_type,
            self._os_type,
            self._mod_version,
            self._mod_flags,
            self._num_pages,
            self._eip_obj,
            self._eip,
            self._esp_obj,
            self._esp,
            self._page_size,
            self._last_page_size,
            self._fixup_sec_size,
            self._fixup_sec_chksum,
            self._loader_sec_size,
            self._loader_sec_chksum,
            self._obj_tbl_offs,
            self._num_objects,
            self._obj_page_tbl_offs,
            self._obj_iter_pages_offs,
            self._rsrc_tbl_offs,
            self._num_rsrc_entries,
            self._resdent_name_tbl_offs,
            self._entry_tbl_offs,
            self._mod_directives_offs,
            self._num_mod_directives,
            self._fixup_page_tbl_offs,
            self._fixup_rec_tbl_offs,
            self._import_mod_tbl_offs,
            self._num_import_mods,
            self._import_proc_tbl_offs,
            self._page_chksum_tbl_offs,
            self._page_data_offs,      # IMPORTANT: This is relative to the file's very beginning.
            self._num_preload_pages,
            self._non_resident_names_tbl_offs,
            self._non_resident_names_tbl_size,
            self._non_resident_names_chksum,
            self._auto_data_obj,
            self._debug_info_offs,
            self._debug_info_len,
            self._num_inst_pages_in_preload,
            self._num_inst_pages_indemand,
            self._heap_size,
        ) = struct.unpack_from("<2sBBLHH40L", data, hdr_offs)

        if self._signature != b'LE':
            raise Exception("Only LE executables are supported.")

    @property
    def hdr_offs(self):
        return self._hdr_offs

    @property
    def byte_order(self):
        return self._byte_order

    @property
    def word_order(self):
        return self._word_order

    @property
    def signature(self):
        return self._signature

    @property
    def level(self):
        return self._level

    @property
    def cpu_type(self):
        return self._cpu_type

    @property
    def os_type(self):
        return self._os_type

    @property
    def mod_version(self):
        return self._mod_version

    @property
    def mod_flags(self):
        return self._mod_flags

    @property
    def num_pages(self):
        return self._num_pages

    @property
    def eip_obj(self):
        return self._eip_obj

    @property
    def eip(self):
        return self._eip

    @property
    def esp_obj(self):
        return self._esp_obj

    @property
    def esp(self):
        return self._esp

    @property
    def page_size(self):
        return self._page_size

    @property
    def last_page_size(self):
        return self._last_page_size

    @property
    def fixup_sec_size(self):
        return self._fixup_sec_size

    @property
    def fixup_sec_chksum(self):
        return self._fixup_sec_chksum

    @property
    def loader_sec_size(self):
        return self._loader_sec_size

    @property
    def loader_sec_chksum(self):
        return self._loader_sec_chksum

    @property
    def obj_tbl_offs(self):
        return self._obj_tbl_offs

    @property
    def num_objects(self):
        return self._num_objects

    @property
    def obj_page_tbl_offs(self):
        return self._obj_page_tbl_offs

    @property
    def obj_iter_pages_offs(self):
        return self._obj_iter_pages_offs

    @property
    def rsrc_tbl_offs(self):
        return self._rsrc_tbl_offs

    @property
    def num_rsrc_entries(self):
        return self._num_rsrc_entries

    @property
    def entry_tbl_offs(self):
        return self._entry_tbl_offs

    @property
    def fixup_page_tbl_offs(self):
        return self._fixup_page_tbl_offs

    @property
    def fixup_rec_tbl_offs(self):
        return self._fixup_rec_tbl_offs

    @property
    def import_mod_tbl_offs(self):
        return self._import_mod_tbl_offs

    @property
    def num_import_mods(self):
        return self._num_import_mods

    @property
    def import_proc_tbl_offs(self):
        return self._import_proc_tbl_offs

    @property
    def page_chksum_tbl_offs(self):
        return self._page_chksum_tbl_offs

    @property
    def page_data_offs(self):
        return self._page_data_offs

    @property
    def non_resident_names_tbl_offs(self):
        return self._non_resident_names_tbl_offs

    @property
    def debug_info_offs(self):
        return self._debug_info_offs

    @property
    def debug_info_size(self):
        return self._debug_info_size

    @property
    def heap_size(self):
        return self._heap_size

    def __repr__(self):
        byte_order = "Little Endian" if self.byte_order == 0 else "Big Endian"
        word_order = "Little Endian" if self.byte_order == 0 else "Big Endian"
        return f"""LE file header (offset in EXE file = 0x{self.hdr_offs:04X}):
    signature = {self.signature}
    byte_order = {byte_order}
    word_order = {word_order}
    level = {self.level}
    cpu_type = {const.CPU_TYPE_MAP[self.cpu_type]}
    os_type = {const.OS_TYPE_MAP[self.os_type]}
    version = {self.mod_version},
    flags = {self.mod_flags},
    num_pages = {self.num_pages}
    start_obj = {self.eip_obj}
    eip = 0x{self.eip:04X}
    stack_obj = {self.esp_obj}
    esp = 0x{self.esp:04X}
    page_size = {self.page_size}
    last_page_size = {self.last_page_size}
    fixup_sec_size = {self.fixup_sec_size}
    fixup_sec_chksum = {self.fixup_sec_chksum}
    loader_sec_size = {self.loader_sec_size}
    loader_sec_chksum = {self.loader_sec_chksum}
    obj_tbl_offs = 0x{self.obj_tbl_offs:04X}
    num_objects = {self.num_objects}
    obj_page_tbl_offs = 0x{self.obj_page_tbl_offs:04X}
    obj_iter_pages_offs = 0x{self.obj_iter_pages_offs:04X}
    rsrc_tbl_offs = {self.rsrc_tbl_offs}
    num_rsrc_entries = {self.num_rsrc_entries}
    entry_off = 0x{self.entry_tbl_offs:04X}
    num_import_mods = {self.num_import_mods}
    import_proc_tbl_offs = 0x{self.import_proc_tbl_offs:04X}
    page_chksum_tbl_offs = 0x{self.page_chksum_tbl_offs:04X}
    page_data_offs = 0x{self.page_data_offs:04X}
    non_resident_names_tbl_offs = 0x{self.non_resident_names_tbl_offs:04X}
    debug_info_offs = 0x{self.debug_info_offs:04X}
    heap_size = 0x{self.heap_size:04X}"""


