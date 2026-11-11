from abc import ABC, abstractmethod
from models.karyawan import Karyawan
from models.payroll_item import UpahLembur
from exceptions.payroll_exception import PayrollCalculationException

class PayrollProcessor(ABC):
    """Kelas dasar berbasis Template Method Pattern."""
    
    def process_payroll(self, karyawan: Karyawan, jam_lembur: float = 0.0) -> dict:
        """Template method utama pengaluran kalkulasi gaji."""
        if karyawan.gaji_pokok < 0:
            raise PayrollCalculationException("Gaji pokok tidak boleh bernilai negatif!")
            
        gaji_kotor = self.hitung_gaji_kotor(karyawan, jam_lembur)
        bpjs_tk, bpjs_kes = self.hitung_bpjs(karyawan.gaji_pokok)
        pph21 = self.hitung_pph21(gaji_kotor * 12)  # Setahun disetahunkan
        
        total_potongan = bpjs_tk + bpjs_kes + pph21
        gaji_bersih = gaji_kotor - total_potongan
        
        return {
            "id_karyawan": karyawan.id_karyawan,
            "nama": karyawan.nama,
            "gaji_kotor": gaji_kotor,
            "bpjs_tk": bpjs_tk,
            "bpjs_kes": bpjs_kes,
            "pph21": pph21,
            "total_potongan": total_potongan,
            "gaji_bersih": gaji_bersih
        }

    @abstractmethod
    def hitung_gaji_kotor(self, karyawan: Karyawan, jam_lembur: float) -> float:
        pass

    @staticmethod
    def hitung_bpjs(gaji_pokok: float):
        bpjs_tk = gaji_pokok * 0.02   # 2% BPJS Ketenagakerjaan
        bpjs_kes = gaji_pokok * 0.01  # 1% BPJS Kesehatan
        return bpjs_tk, bpjs_kes

    @staticmethod
    def hitung_pph21(pkp_tahunan: float) -> float:
        """Static Method perhitungan PPh21 Progresif."""
        if pkp_tahunan <= 0:
            return 0.0
        elif pkp_tahunan <= 60000000:
            return (pkp_tahunan * 0.05) / 12
        elif pkp_tahunan <= 250000000:
            return (3000000 + (pkp_tahunan - 60000000) * 0.15) / 12
        else:
            return (31500000 + (pkp_tahunan - 250000000) * 0.25) / 12


class StandardPayrollProcessor(PayrollProcessor):
    """Implementasi konkrit dari Template Method."""
    def hitung_gaji_kotor(self, karyawan: Karyawan, jam_lembur: float) -> float:
        tarif_lembur = 25000.0
        lembur_item = UpahLembur("L01", "Lembur", jam_lembur, tarif_lembur, karyawan.id_karyawan)
        return karyawan.gaji_pokok + lembur_item.hitung_total()