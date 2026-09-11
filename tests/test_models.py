import unittest

from risk_language import (
    black_scholes_call_price,
    black_scholes_call_risk,
    option_pnl,
    rates_pnl,
    zero_coupon_price,
    zero_coupon_risk,
)


class BlackScholesTests(unittest.TestCase):
    def test_standard_at_the_money_benchmark(self) -> None:
        risk = black_scholes_call_risk(100.0, 100.0, 0.05, 0.20, 1.0)

        self.assertAlmostEqual(risk.price, 10.450584, places=5)
        self.assertAlmostEqual(risk.delta, 0.636831, places=5)
        self.assertAlmostEqual(risk.gamma, 0.018762, places=5)

    def test_second_order_beats_linear_for_small_move(self) -> None:
        inputs = (100.0, 100.0, 0.05, 0.20, 1.0)
        risk = black_scholes_call_risk(*inputs)
        move = 1.0
        exact = black_scholes_call_price(101.0, *inputs[1:]) - risk.price
        approx = option_pnl(risk.delta, risk.gamma, move)

        self.assertLess(abs(exact - approx.total), abs(exact - approx.linear))


class ZeroCouponTests(unittest.TestCase):
    def test_price_and_risk_are_analytic(self) -> None:
        risk = zero_coupon_risk(1_000.0, 0.04, 5.0)

        self.assertAlmostEqual(risk.price, 821.927107, places=5)
        self.assertAlmostEqual(risk.modified_duration, 5.0 / 1.04)
        self.assertAlmostEqual(risk.dv01, risk.modified_duration * risk.price / 10_000)
        self.assertAlmostEqual(risk.dollar_convexity, risk.convexity * risk.price)

    def test_second_order_beats_linear_for_small_yield_move(self) -> None:
        risk = zero_coupon_risk(1_000.0, 0.04, 5.0)
        move_bp = 10.0
        exact = zero_coupon_price(1_000.0, 0.041, 5.0) - risk.price
        approx = rates_pnl(risk.dv01, risk.dollar_convexity, move_bp)

        self.assertLess(abs(exact - approx.total), abs(exact - approx.linear))

    def test_rejects_yield_outside_domain(self) -> None:
        with self.assertRaises(ValueError):
            zero_coupon_price(1_000.0, -1.0, 5.0)


if __name__ == "__main__":
    unittest.main()

