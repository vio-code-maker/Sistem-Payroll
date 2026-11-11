import csv

class PayrollCSVExporter:
    """Kelas khusus menangani ekspor laporan ke CSV (Penerapan SRP)."""
    @staticmethod
    def ekspor_laporan(nama_file: str, data_slip: list) -> bool:
        try:
            with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID Karyawan", "Nama", "Gaji Kotor", "BPJS TK", "BPJS Kes", "PPh21", "Total Potongan", "Gaji Bersih"])
                for s in data_slip:
                    writer.writerow([
                        s['id_karyawan'], s['nama'], s['gaji_kotor'], 
                        s['bpjs_tk'], s['bpjs_kes'], s['pph21'], 
                        s['total_potongan'], s['gaji_bersih']
                    ])
            return True
        except Exception:
            return False