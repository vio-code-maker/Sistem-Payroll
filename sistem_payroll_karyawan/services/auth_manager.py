from models.karyawan import Karyawan

class AuthManager:
    def __init__(self):
        self._daftar_karyawan = {}
        self._current_user = None

    def registrasi(self, karyawan: Karyawan) -> bool:
        if karyawan.username in self._daftar_karyawan:
            return False
        self._daftar_karyawan[karyawan.username] = karyawan
        return True

    def login(self, username: str, password: str) -> bool:
        user = self._daftar_karyawan.get(username)
        if user and user.password == password:
            self._current_user = user
            return True
        return False

    def logout(self) -> bool:
        self._current_user = None
        return True

    @property
    def current_user(self):
        return self._current_user