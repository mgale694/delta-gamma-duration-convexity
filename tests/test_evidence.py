import math
import unittest

from research.sweep import bond_rows, call_rows, coupon_risk, crossings, experiments, scaled_calls
from risk_language import black_scholes_call_price, black_scholes_call_risk, zero_coupon_risk


class ResearchChecks(unittest.TestCase):
    def test_coupon_strip_matches_par_and_bumped_annuity(self):
        def annuity(y):
            discount = (1 + y) ** -5
            return 40 * (1 - discount) / y + 1000 * discount

        y, h = .04, .00001
        risk = coupon_risk(5, y, .04)
        self.assertAlmostEqual(risk.price, 1000)
        self.assertAlmostEqual(risk.dv01, (annuity(y-h)-annuity(y+h))/(2*h*10000), places=7)
        self.assertAlmostEqual(risk.dollar_convexity, (annuity(y+h)-2*annuity(y)+annuity(y-h))/h**2, delta=.1)

    def test_cme_style_centered_dv01(self):
        for years in (2, 5, 10, 30):
            bumped = (1000 / 1.0399**years - 1000 / 1.0401**years) / 2
            self.assertAlmostEqual(zero_coupon_risk(1000, .04, years).dv01, bumped, delta=.000002)

    def test_call_finite_differences(self):
        for years in (7/365, 1):
            risk = black_scholes_call_risk(100, 100, .05, .2, years)
            h = .005
            up, down = (black_scholes_call_price(s, 100, .05, .2, years) for s in (100+h, 100-h))
            self.assertAlmostEqual(risk.delta, (up-down)/(2*h), places=6)
            self.assertAlmostEqual(risk.gamma, (up+down-2*risk.price)/h**2, places=6)

    def test_stress_prices_against_integrated_payoff(self):
        # Independent normal integration above the exercise boundary, Simpson's rule.
        for years in (7/365, 1):
            vol_time = .2 * math.sqrt(years)
            drift = (.05 - .2**2/2) * years
            for spot in (80, 90, 100, 110, 120):
                lower = (math.log(100/spot) - drift) / vol_time
                step = (12 - lower) / 4000
                def integrand(z):
                    payoff = spot * math.exp(drift + vol_time*z) - 100
                    return payoff * math.exp(-z*z/2) / math.sqrt(2*math.pi)
                weighted = integrand(lower) + integrand(12)
                for i in range(1, 4000):
                    weighted += (4 if i % 2 else 2) * integrand(lower + step*i)
                value = math.exp(-.05*years) * step * weighted / 3
                self.assertAlmostEqual(value, black_scholes_call_price(spot, 100, .05, .2, years), places=8)

    def test_sweep_invariants(self):
        for rows in experiments():
            self.assertEqual(len({r['shock'] for r in rows}), 401)
            for r in rows:
                self.assertGreaterEqual(r['exact'] + 1e-10, r['linear'])
                if r['shock'] == 0:
                    self.assertEqual((r['exact'], r['linear'], r['second']), (0, 0, 0))
                    self.assertIsNone(r['linear_error_pct'])
                else:
                    self.assertTrue(math.isfinite(r['second_error_pct']))

    def test_crossings_use_first_sample_outward(self):
        results = list(crossings(list(bond_rows(5))))
        for r in results:
            if r['tolerance_pct'] == 1:
                expected = 35*r['direction'] if r['approximation'] == 'linear' else None
                self.assertEqual(r['first_sample_above'], expected)

    def test_scaled_shock_matches_grid_for_one_year(self):
        row = next(r for r in scaled_calls() if r['case'] == 'call-1y' and r['vol_scale_multiple'] == -.5)
        reference = next(r for r in call_rows('call-1y', 1) if r['shock'] == -10)
        self.assertAlmostEqual(row['second_error_pct'], reference['second_error_pct'])

    def test_frozen_gamma_can_reverse_the_sign(self):
        row = next(r for r in call_rows('call-7d', 7/365) if r['shock'] == -10)
        self.assertLess(row['exact'], 0)
        self.assertGreater(row['second'], 0)
