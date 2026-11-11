
from datetime import datetime
from models.absensi import (
    Absensi,
    PerhitunganJamKerja,
    PengecekanKeterlambatan
)


class AbsensiManager:
    def __init__(self, batas_jam_masuk: str = "08:00"):
        self._perhitungan = PerhitunganJamKerja()
        self._pengecekan = PengecekanKeterlambatan(batas_jam_masuk)

    def absen_masuk(
        self,
        daftar_absensi: list[Absensi],
        id_karyawan: str,
        tanggal: str,
        jam_masuk: str
    ):
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            datetime.strptime(jam_masuk, "%H:%M")
        except ValueError:
            return False, "Format tanggal atau jam tidak valid!"
        for absensi in daftar_absensi:
            if (
                absensi.id_karyawan == id_karyawan
                and absensi.tanggal == tanggal
            ):
                return False, "Anda sudah melakukan absensi pada tanggal tersebut!"
        id_absensi = f"A{len(daftar_absensi) + 1:03d}"
        absensi = Absensi(
            id_absensi,
            id_karyawan,
            tanggal,
            jam_masuk
        )
        daftar_absensi.append(absensi)
        return True, "Absensi masuk berhasil!"

    def absen_keluar(
        self,
        daftar_absensi: list[Absensi],
        id_karyawan: str,
        tanggal: str,
        jam_keluar: str
    ):
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            datetime.strptime(jam_keluar, "%H:%M")
        except ValueError:
            return False, "Format tanggal atau jam tidak valid!"
        for absensi in daftar_absensi:
            if (
                absensi.id_karyawan == id_karyawan
                and absensi.tanggal == tanggal
                and absensi.jam_keluar is None
            ):
                if jam_keluar <= absensi.jam_masuk:
                    return False, "Jam keluar harus setelah jam masuk!"
                absensi.catat_check_out(jam_keluar)
                return True, "Absensi keluar berhasil!"
        return False, "Data absensi masuk tidak ditemukan atau sudah check-out."

    def hitung_jam_kerja_harian(
        self,
        daftar_absensi: list[Absensi],
        id_karyawan: str,
        tanggal: str
    ) -> float:
        for absensi in daftar_absensi:
            if (
                absensi.id_karyawan == id_karyawan
                and absensi.tanggal == tanggal
            ):
                return self._perhitungan.hitung_jam_kerja(absensi)
        return 0.0

    def cek_keterlambatan(
        self,
        daftar_absensi: list[Absensi],
        id_karyawan: str,
        tanggal: str
    ):
        for absensi in daftar_absensi:
            if (
                absensi.id_karyawan == id_karyawan
                and absensi.tanggal == tanggal
            ):
                terlambat = self._pengecekan.cek_keterlambatan(absensi)
                if terlambat:
                    return True, "Karyawan terlambat."
                else:
                    return False, "Karyawan datang tepat waktu."
        return None, "Data absensi tidak ditemukan."
