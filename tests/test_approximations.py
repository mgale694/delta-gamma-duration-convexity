import math
import unittest

from risk_language import option_pnl, rates_pnl


class OptionPnLTests(unittest.TestCase):
    def test_breaks_pnl_into_linear_and_curvature_terms(self) -> None:
        result = option_pnl(delta=0.55, gamma=0.04, spot_change=2.0)

        self.assertAlmostEqual(result.linear, 1.10)
        self.assertAlmostEqual(result.curvature, 0.08)
        self.assertAlmostEqual(result.total, 1.18)

    def test_rejects_non_finite_inputs(self) -> None:
        with self.assertRaises(ValueError):
            option_pnl(delta=math.nan, gamma=0.04, spot_change=2.0)


class RatesPnLTests(unittest.TestCase):
    def test_uses_positive_dv01_loss_convention_and_decimal_convexity(self) -> None:
        result = rates_pnl(
            dv01=1_250.0,
            dollar_convexity=80_000_000.0,
            yield_change_bp=10.0,
        )

        self.assertAlmostEqual(result.linear, -12_500.0)
        self.assertAlmostEqual(result.curvature, 40.0)
        self.assertAlmostEqual(result.total, -12_460.0)

    def test_rejects_negative_dv01_magnitude(self) -> None:
        with self.assertRaises(ValueError):
            rates_pnl(-1.0, 10.0, 1.0)


if __name__ == "__main__":
    unittest.main()

