class Karyawan:
    def __init__(self, id_karyawan: str, nama: str, jabatan: str, departemen: str, gaji_pokok: float, username: str, password: str):
        self._id_karyawan = id_karyawan
        self._nama = nama
        self._jabatan = jabatan
        self._departemen = departemen
        self._gaji_pokok = gaji_pokok
        self._username = username
        self._password = password

    @property
    def id_karyawan(self) -> str:
        return self._id_karyawan

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def jabatan(self) -> str:
        return self._jabatan

    @property
    def departemen(self) -> str:
        return self._departemen

    @property
    def gaji_pokok(self) -> float:
        return self._gaji_pokok

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @classmethod
    def dari_dict(cls, data: dict):
        """Class Method untuk instansiasi objek dari dictionary."""
        return cls(
            id_karyawan=data['id_karyawan'],
            nama=data['nama'],
            jabatan=data['jabatan'],
            departemen=data['departemen'],
            gaji_pokok=data['gaji_pokok'],
            username=data['username'],
            password=data['password']
        )