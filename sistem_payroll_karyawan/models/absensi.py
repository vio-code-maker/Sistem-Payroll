class Absensi:
    def __init__(self, id_absensi: str,id_karyawan: str, tanggal: str, jam_masuk: str, jam_keluar: str = None):
        self._id_absensi = id_absensi
        self._id_karyawan = id_karyawan
        self._tanggal = tanggal
        self._jam_masuk = jam_masuk
        self._jam_keluar = jam_keluar

    @property
    def id_karyawan(self) -> str:
        return self._id_karyawan

    @property
    def tanggal(self) -> str:
        return self._tanggal
        
    @property
    def jam_masuk(self) -> str:
        return self._jam_masuk

    @property
    def jam_keluar(self) -> str:
        return self._jam_keluar

    def catat_check_out(self, jam_keluar: str):
        self._jam_keluar = jam_keluar


class PerhitunganJamKerja:
    @staticmethod
    def hitung_jam_kerja(absensi: Absensi) -> float:
        if not absensi.jam_keluar:
            return 0.0
        # Simulasi sederhana konversi jam "HH:MM" ke selisih jam
        masuk_jam, masuk_mnt = map(int, absensi.jam_masuk.split(":"))
        keluar_jam, keluar_mnt = map(int, absensi.jam_keluar.split(":"))
        total_jam = (keluar_jam + keluar_mnt / 60) - (masuk_jam + masuk_mnt / 60)
        return max(0.0, total_jam)


class PengecekanKeterlambatan:
    def __init__(self, batas_jam_masuk: str = "08:00"):
        self._batas_jam_masuk = batas_jam_masuk

    def cek_keterlambatan(self, absensi: Absensi) -> bool:
        return absensi.jam_masuk > self._batas_jam_masuk