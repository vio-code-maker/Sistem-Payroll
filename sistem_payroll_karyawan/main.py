from models.karyawan import Karyawan
from models.absensi import Absensi
from services.payroll_processor import StandardPayrollProcessor
from services.iterators import DepartemenKaryawanIterator
from services.exporters import PayrollCSVExporter
from services.auth_manager import AuthManager
from services.absensi_manager import AbsensiManager
def main():
 
    processor = StandardPayrollProcessor()
    auth = AuthManager()
    absensiManager= AbsensiManager(batas_jam_masuk = '08:00')

    # Data Sampel Karyawan (Kelompok 10) = 
    default = Karyawan(
        "K000",
        "Admin Hrd",
        "HRD",
        "HRD",
        8000000,
        "hrd",
        "hrd123"
    )
    auth.registrasi(default)
    daftar_karyawan = auth._daftar_karyawan
    daftar_absensi: list[Absensi] = []

    while True:
        print("\n")
        print("+------------------------------------------------------------+")
        print("|          SISTEM MANAJEMEN KARYAWAN & PAYROLL               |")
        print("|                 KELOMPOK 10 - MIKROSKIL                    |")
        print("+------------------------------------------------------------+")
        print("| [1] Login                                                  |")
        print("| [2] Logout                                                 |")
        print("| [3] Keluar Program                                         |")
        print("+------------------------------------------------------------+")
        
        pilihan = input("\n> Masukkan pilihan menu (1-3): ").strip()
        if pilihan == "1":
            if auth.current_user is not None:
                print("Anda sudah login!")
                continue
            print("Masukkan Username dan Password untuk login")
            usn=input("Masukkan Username: ")
            pw= input("Masukkan Password:")
            if auth.login(usn, pw):
                user = auth.current_user
                print(f"Login berhasil! Selamat datang {user.nama}!")
                print(f"Jabatan: {user.jabatan}, Departemen: {user.departemen}")
            else:
                print("Login gagal!")
                input("\nTekan [Enter] untuk kembali ke menu login...")
                continue
        elif pilihan == "2":
            auth.logout()
            print("Logout berhasil!")
            continue
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan sistem payroll Kelompok 10. Sampai jumpa!\n")
            break
 
        while True:
            print("\n")
            print("+------------------------------------------------------------+")
            print("|          SISTEM MANAJEMEN KARYAWAN & PAYROLL               |")
            print("|                 KELOMPOK 10 - MIKROSKIL                    |")
            print("+------------------------------------------------------------+")
            print("| [1] Registrasi Karyawan                                    |")
            print("| [2] Lihat Daftar Karyawan (Tabel Kotak)                    |")
            print("| [3] Proses Hitung Payroll & Cetak Slip Gaji                |")
            print("| [4] Ekspor Laporan Payroll ke CSV (SRP)                    |")
            print("| [5] Cek Karyawan per Departemen (Iterator Pattern)         |")
            print("| [6] Absensi                                                |")
            print("| [7] Keluar Program                                         |")
            print("+------------------------------------------------------------+")
        
            pilihan = input("\n> Masukkan pilihan menu (1-6): ").strip()

            if pilihan == "1":
                if user and user._jabatan.upper() == "HRD" or user._jabatan.upper() == "ADMIN":
                    jlhData = int(input("Jumlah data karyawan yang mau di register: "))
                    for i in range (1,jlhData+1):
                        print("Masukkan karyawan ke -", i)
                        idKaryawan=input("Masukkan ID Karyawan: ")
                        namaLengkap=input("Masukkan Nama Lengkap: ")
                        jabatan=input("Masukkan Jabatan: ")
                        departemen=input("Masukkan Departemen: ")
                        gajiPokok=float(input("Masukkan Gaji Pokok: "))
                        username=input("Masukkan Username: ")
                        password=input("Masukkan Password: ")
                        karyawan = Karyawan(idKaryawan,namaLengkap,jabatan,departemen,gajiPokok,username,password)

                        if auth.registrasi(karyawan):
                            print("Karyawan berhasil diregister!")
                        else:
                            print("Gagal register, username sudah terdaftar!")
                        continue
                else:
                    print("Anda tidak memiliki akses untuk melakukan registrasi!")
                input("\nTekan [Enter] untuk kembali ke menu utama...")
                continue
 
            elif pilihan == "2":
                if user and  user._jabatan.upper() == "HRD" or user._jabatan.upper() == "ADMIN" or user._jabatan.upper() == "SPV":
                    print("\n┌──────┬────────────────────┬────────────────────┬──────────────┬────────────────┐")
                    print("│  ID  │ Nama Lengkap       │ Jabatan            │ Departemen   │ Gaji Pokok     │")
                    print("├──────┼────────────────────┼────────────────────┼──────────────┼────────────────┤")
                    for k in daftar_karyawan.values():
                        gaji_str = f"Rp {k.gaji_pokok:,.0f}"
                        print(f"│ {k.id_karyawan:<4} │ {k.nama:<18} │ {k._jabatan:<18} │ {k.departemen:<12} │ {gaji_str:>14} │")
                        print("└──────┴────────────────────┴────────────────────┴──────────────┴────────────────┘")
                else:
                    print("Anda tidak memiliki akses untuk melihat daftar karyawan!")
                input("\nTekan [Enter] untuk kembali ke menu utama...")
                continue
 
            elif pilihan == "3":
                if user and user._jabatan.upper() == "FINANCE" or user._jabatan.upper() == "ADMIN":
                    print("\n┌──────────────────────────────────────────────────┐")
                    print("│          PROSES PERHITUNGAN GAJI & SLIP          │")
                    print("└──────────────────────────────────────────────────┘")
                    id_cari = input("Masukkan ID Karyawan (Contoh: K001): ").strip()
                    karyawan = next((k for k in daftar_karyawan.values() if k.id_karyawan == id_cari), None)
            
                    if karyawan:
                        try:
                            lembur_input = input("Masukkan jumlah jam lembur (Kosongkan jika 0): ").strip()
                            lembur = float(lembur_input) if lembur_input else 0.0
                    
                            slip = processor.process_payroll(karyawan, jam_lembur=lembur)
                    
                            g_kotor = f"Rp {slip['gaji_kotor']:,.2f}"
                            b_tk = f"Rp {slip['bpjs_tk']:,.2f}"
                            b_kes = f"Rp {slip['bpjs_kes']:,.2f}"
                            pph = f"Rp {slip['pph21']:,.2f}"
                            t_pot = f"Rp {slip['total_potongan']:,.2f}"
                            g_bersih = f"Rp {slip['gaji_bersih']:,.2f}"
 
                            print("\n┌──────────────────────────────────────────────┐")
                            print("│               SLIP GAJI PEGAWAI              │")
                            print("├──────────────────────────────────────────────┤")
                            print(f"│ Nama Pegawai  : {slip['nama']:<27} │")
                            print(f"│ ID Karyawan   : {slip['id_karyawan']:<27} │")
                            print("├──────────────────────────────────────────────┤")
                            print(f"│ Gaji Kotor    : {g_kotor:>26} │")
                            print(f"│ - BPJS TK 2%  : {b_tk:>26} │")
                            print(f"│ - BPJS Kes 1% : {b_kes:>26} │")
                            print(f"│ - PPh 21 Prog : {pph:>26} │")
                            print(f"│ Total Potongan: {t_pot:>26} │")
                            print("├──────────────────────────────────────────────┤")
                            print(f"│ GAJI BERSIH   : {g_bersih:>26} │")
                            print("└──────────────────────────────────────────────┘")
                        except ValueError:
                            print("[!] Error: Masukkan angka jam lembur yang valid!")
                    else:
                        print("[!] Karyawan dengan ID tersebut tidak ditemukan!")
                    input("\nTekan [Enter] untuk kembali ke menu utama...")
                    continue
                else:
                    print("Anda tidak memiliki akses untuk melakukan proses perhitungan gaji!")
                input("\nTekan [Enter] untuk kembali ke menu utama...")
                continue
 
            elif pilihan == "4":
                if user and user._jabatan.upper() == "FINANCE" or user._jabatan.upper() == "ADMIN" or user._jabatan.upper() == "HEAD" or user._jabatan.upper() == "SPV":
                    print("\n┌──────────────────────────────────────────────────────────┐")
                    print("│           EKSPOR LAPORAN PAYROLL KE FORMAT CSV           │")
                    print("└──────────────────────────────────────────────────────────┘")
                    semua_slip = [processor.process_payroll(k, jam_lembur=5.0) for k in daftar_karyawan.values()]
                    nama_file = "laporan_payroll_perusahaan.csv"
            
                    if PayrollCSVExporter.ekspor_laporan(nama_file, semua_slip):
                        print(f"[+] [BERHASIL] Laporan berhasil diekspor ke file '{nama_file}'!")
                        print("    Catatan: Penerapan prinsip SOLID (Single Responsibility Principle)")
                        print("    memisahkan tugas ekspor file ke kelas tersendiri secara bersih.")
                    else:
                        print("[-] Gagal mengekspor file.")
                    input("\nTekan [Enter] untuk kembali ke menu utama...")
                    continue
                else:
                    print("Anda tidak memiliki akses untuk mengekspor laporan payroll!")
                input("\nTekan [Enter] untuk kembali ke menu utama...")
                continue
 
            elif pilihan == "5":
                if user and user._jabatan.upper() == "HRD" or user._jabatan.upper() == "ADMIN":
                    print("\n┌──────────────────────────────────────────────────┐")
                    print("│     TRAVERSAL KARYAWAN PER DEPARTEMEN (ITERATOR) │")
                    print("└──────────────────────────────────────────────────┘")
                    dept = input("Masukkan nama departemen (Contoh: IT, HRD, Finance): ").strip()
                    iterator = DepartemenKaryawanIterator(daftar_karyawan.values(), dept)
            
                    judul_dept = f"Anggota Departemen [{dept.upper()}]"
                    print("\n┌──────────────────────────────────────────┐")
                    print(f"│ {judul_dept:<40} │")
                    print("├──────────────────────────────────────────┤")
                    count = 0
                    for emp in iterator:
                        teks_pegawai = f"- [{emp.id_karyawan}] {emp.nama}"
                        print(f"│ {teks_pegawai:<40} │")
                        count += 1
                    if count == 0:
                        teks_kosong = "[-] Tidak ada karyawan ditemukan."
                        print(f"│ {teks_kosong:<40} │")
                    print("└──────────────────────────────────────────┘")
                    input("\nTekan [Enter] untuk kembali ke menu utama...")
                    continue
                else:
                    print("Anda tidak memiliki akses untuk melakukan traversal karyawan per departemen!")
                input("\nTekan [Enter] untuk kembali ke menu utama...")
                continue
            elif pilihan == "6":
                id_karyawan = user._id_karyawan
                while True:
                    print("\n")
                    print("+------------------------------------------------------------+")
                    print("|                  SISTEM ABSENSI KARYAWAN                   |")
                    print("|                 KELOMPOK 10 - MIKROSKIL                    |")
                    print("+------------------------------------------------------------+")
                    print("| [1] Absensi Masuk                                          |")
                    print("| [2] Absensi Keluar                                         |")
                    print("| [3] Hitung Jam Kerja Harian                                |")
                    print("| [4] Cek Keterlambatan                                      |")
                    print("| [5] Keluar dari Sub Menu Absensi                           |")
                    print("+------------------------------------------------------------+")

                    pilihan = input("Pilih menu: ")

                    if pilihan == "1":
                        tanggal = input("Tanggal (YYYY-MM-DD): ")
                        jam_masuk = input("Jam masuk (HH:MM): ")

                        berhasil, pesan = absensiManager.absen_masuk(
                            daftar_absensi, id_karyawan, tanggal, jam_masuk
                        )
                        print(pesan)
                        continue
                    elif pilihan == "2":
                        tanggal = input("Tanggal (YYYY-MM-DD): ")
                        jam_keluar = input("Jam keluar (HH:MM): ")

                        berhasil, pesan = absensiManager.absen_keluar(
                            daftar_absensi, id_karyawan, tanggal, jam_keluar
                        )
                        print(pesan)
                        continue

                    elif pilihan == "3":
                        if user and user._jabatan.upper() == "ADMIN" or user._jabatan.upper() == "SPV":
                            id_karyawan = input("Masukkan Id Karyawan Yang Mau Di Hitung Jam Kerjanya: ")
                            tanggal = input("Tanggal (YYYY-MM-DD): ")

                            total_jam = absensiManager.hitung_jam_kerja_harian(
                                daftar_absensi, id_karyawan, tanggal
                            )
                            print(f"Total jam kerja: {total_jam:.2f} jam")
                            continue
                        else:
                            print("Anda tidak memiliki akses untuk melakukan perhitungan jam kerja!")
                        input("\nTekan [Enter] untuk kembali ke menu utama...")
                        continue
                    elif pilihan == "4":
                        if user and user._jabatan.upper() == "ADMIN" or user._jabatan.upper() == "SPV":
                            id_karyawan = input("Masukkan Id Karyawan Yang Mau Di Hitung Jam Kerjanya: ")
                            tanggal = input("Tanggal (YYYY-MM-DD): ")

                            terlambat, pesan = absensiManager.cek_keterlambatan(
                                daftar_absensi, id_karyawan, tanggal
                            )
                            print(pesan)
                            continue
                        else:
                            print("Anda tidak memiliki akses untuk melakukan perhitungan keterlambatan!")
                        input("\nTekan [Enter] untuk kembali ke menu utama...")
                        continue
                    elif pilihan == "5":
                        print("\nKeluar dari sub menu absensi...")
                        break
                    else:
                        print("Pilihan tidak valid!")
                        continue
                    input("\nTekan [Enter] untuk kembali ke menu utama...")
            elif pilihan == "7":
                print("\nTerima kasih telah menggunakan sistem payroll Kelompok 10. Sampai jumpa!\n")
                break
            else:
                print("[!] Pilihan tidak valid! Silakan masukkan angka 1 sampai 5.")
 
if __name__ == "__main__":
    main()