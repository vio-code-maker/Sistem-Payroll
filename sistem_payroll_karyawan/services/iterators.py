class DepartemenKaryawanIterator:
    """Iterator Pattern untuk menelusuri karyawan berdasarkan departemen."""
    def __init__(self, daftar_karyawan: list, target_departemen: str):
        self._daftar = [k for k in daftar_karyawan if k.departemen.lower() == target_departemen.lower()]
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._daftar):
            item = self._daftar[self._index]
            self._index += 1
            return item
        raise StopIteration