class PayrollCalculationException(Exception):
    """Custom Exception untuk validasi perhitungan error pada payroll."""
    def __init__(self, pesan="Terjadi kesalahan dalam perhitungan payroll."):
        super().__init__(pesan)