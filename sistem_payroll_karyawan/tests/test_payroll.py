import pytest
from models.karyawan import Karyawan
from models.payroll_item import UpahLembur
from services.payroll_processor import StandardPayrollProcessor
from services.iterators import DepartemenKaryawanIterator
from services.exporters import PayrollCSVExporter
from exceptions.payroll_exception import PayrollCalculationException

def test_hitung_upah_lembur():
    lembur = UpahLembur("L1", "Lembur Proyek", 10.0, 20000.0, "K001")
    assert lembur.hitung_total() == 200000.0

def test_karyawan_property():
    k = Karyawan("K001", "Angela Yulia", "Senior Developer", "IT", 8500000.0, "angela", "123")
    assert k.id_karyawan == "K001"
    assert k.nama == "Angela Yulia"
    assert k.gaji_pokok == 8500000.0
    assert k.departemen == "IT"

def test_hitung_bpjs():
    proc = StandardPayrollProcessor()
    tk, kes = proc.hitung_bpjs(5000000.0)
    assert tk == 100000.0
    assert kes == 50000.0

def test_pph21_progresif():
    pajak = StandardPayrollProcessor.hitung_pph21(60000000.0)
    assert pajak > 0

def test_payroll_exception():
    with pytest.raises(PayrollCalculationException):
        proc = StandardPayrollProcessor()
        bad_user = Karyawan("K99", "Error User", "Staff", "IT", -1000.0, "err", "123")
        proc.process_payroll(bad_user, jam_lembur=0.0)

def test_karyawan_dari_dict():
    data = {
        "id_karyawan": "K999", "nama": "Test User", "jabatan": "Staff",
        "departemen": "IT", "gaji_pokok": 4000000.0, "username": "test", "password": "123"
    }
    k = Karyawan.dari_dict(data)
    assert k.id_karyawan == "K999"
    assert k.nama == "Test User"

def test_iterator_departemen():
    daftar = [
        Karyawan("K001", "Angela", "Dev", "IT", 5000000.0, "a", "1"),
        Karyawan("K002", "Catrina", "HR", "HRD", 5000000.0, "c", "1")
    ]
    iterator = DepartemenKaryawanIterator(daftar, "IT")
    hasil = list(iterator)
    assert len(hasil) == 1
    assert hasil[0].nama == "Angela"

def test_csv_exporter(tmp_path):
    file_path = tmp_path / "test_laporan.csv"
    data = [{
        "id_karyawan": "K001", "nama": "Angela", "gaji_kotor": 5000000,
        "bpjs_tk": 100000, "bpjs_kes": 50000, "pph21": 200000,
        "total_potongan": 350000, "gaji_bersih": 4650000
    }]
    hasil = PayrollCSVExporter.ekspor_laporan(str(file_path), data)
    assert hasil is True

def test_standard_payroll_processor():
    k = Karyawan("K001", "Angela Yulia", "Dev", "IT", 6000000.0, "angela", "123")
    proc = StandardPayrollProcessor()
    slip = proc.process_payroll(k, jam_lembur=5.0)
    assert slip["id_karyawan"] == "K001"
    assert slip["gaji_kotor"] > 6000000.0

def test_payroll_item_abstract():
    with pytest.raises(TypeError):
        from models.payroll_item import PayrollItem
        PayrollItem("ID", "Test", 100.0)