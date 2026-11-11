from abc import ABC, abstractmethod

class PayrollItem(ABC):
    """Kelas abstrak komponen payroll (Inheritance & Abstraction)."""
    def __init__(self, id_item: str, nama: str, jumlah: float):
        self._id_item = id_item
        self._nama = nama
        self._jumlah = jumlah

    @property
    def nama(self) -> str:
        return self._nama

    @abstractmethod
    def hitung_total(self) -> float:
        """Method abstrak yang wajib di-override oleh child class (Polymorphism)."""
        pass

class GajiPokok(PayrollItem):
    """Child class Gaji Pokok mewarisi PayrollItem."""
    def __init__(self, id_item: str, nama: str, jumlah: float, periode: str, id_karyawan: str):
        super().__init__(id_item, nama, jumlah)
        self._periode = periode
        self._id_karyawan = id_karyawan

    def hitung_total(self) -> float:
        return self._jumlah

class UpahLembur(PayrollItem):
    """Child class Upah Lembur mewarisi PayrollItem."""
    def __init__(self, id_item: str, nama: str, jam_lembur: float, tarif_per_jam: float, id_karyawan: str):
        super().__init__(id_item, nama, jumlah=0.0)
        self._jam_lembur = jam_lembur
        self._tarif_per_jam = tarif_per_jam
        self._id_karyawan = id_karyawan

    def hitung_total(self) -> float:
        """Override method abstrak untuk kalkulasi upah lembur."""
        return self._jam_lembur * self._tarif_per_jam