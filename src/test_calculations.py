import pytest
from dtd_calculator import AVCalculator
import numpy as np

# Mock class that doesn't load a CSV file
class MockAVCalculator(AVCalculator):
    def __init__(self):
        pass

def test_compute_liabilities():
    calc = MockAVCalculator()
    row = {
        'Short Term Debt': 20,
        'Long Term Debt': 40,
        'Other Liability': 10
    }
    result = calc.compute_liabilities(row)
    expected = 20 + 0.5 * 40 + 0.3466 * 10
    print(f"[Liability Calculation] Expected: {expected:.4f}, Got: {result:.4f}")
    assert abs(result - expected) < 1e-6

def test_d1_d2():
    calc = MockAVCalculator()
    V, L, r = 100, 80, 0.02
    d1, d2 = calc.d1_d2(V, L, r)
    print(f"[d1/d2] V: {V}, L: {L}, r: {r}")
    print(f"→ d1: {d1:.4f}, d2: {d2:.4f}")
    assert isinstance(d1, float)
    assert isinstance(d2, float)
    assert d1 > d2

def test_equity_formula():
    calc = MockAVCalculator()
    V, L, r = 100, 80, 0.02
    E = calc.equity_formula(V, L, r)
    print(f"[Equity Formula] V: {V}, L: {L}, r: {r} → E: {E:.4f}")
    assert E > 0

def test_newton_raphson_success():
    calc = MockAVCalculator()
    E, L, r = 50, 40, 0.02
    V, success = calc.newton_raphson(E, L, r)
    print(f"[Newton-Raphson] E: {E}, L: {L}, r: {r} → V: {V:.4f}, Success: {success}")
    assert success
    assert V > L

def test_dtd_calculation():
    calc = MockAVCalculator()
    V, L = 100, 80
    dtd = calc.calculate_dtd(V, L)
    print(f"[DTD Calculation] V: {V}, L: {L} → DTD: {dtd:.4f}")
    assert isinstance(dtd, float)
    assert dtd > 0

def test_full_row_computation():
    class MiniCalc(AVCalculator):
        def __init__(self):
            self.results = []

        def run_single(self, row):
            E = row['Market Capitalization']
            r = row['Daily Risk-Free Rate'] * 250
            L = self.compute_liabilities(row)
            V, success = self.newton_raphson(E, L, r)
            dtd = self.calculate_dtd(V, L) if success else np.nan
            return E, L, r, V, success, dtd

    calc = MiniCalc()
    fake_row = {
        'Market Capitalization': 100,
        'Short Term Debt': 30,
        'Long Term Debt': 40,
        'Other Liability': 20,
        'Daily Risk-Free Rate': 0.0001
    }
    E, L, r, V, success, dtd = calc.run_single(fake_row)
    print(f"[Full Computation] E: {E}, L: {L:.2f}, r: {r:.4f}")
    print(f"→ V: {V:.4f}, Success: {success}, DTD: {dtd:.4f}")
    assert success
    assert dtd > 0