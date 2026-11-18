"""Reproduce the one-factor, frozen-sensitivity experiments from the repository root."""
import csv
from math import sqrt
from pathlib import Path

from risk_language import (
    RatesRisk, black_scholes_call_risk, black_scholes_call_price,
    option_pnl, rates_pnl, zero_coupon_price, zero_coupon_risk,
)


def coupon_risk(years, y, coupon):
    """Value the coupon bond on a coupon date as a strip of annual cash flows."""
    strips = [zero_coupon_risk(1000 * coupon, y, t) for t in range(1, years + 1)]
    strips.append(zero_coupon_risk(1000, y, years))
    price = sum(s.price for s in strips)
    dv01 = sum(s.dv01 for s in strips)
    curvature = sum(s.dollar_convexity for s in strips)
    return RatesRisk(price, dv01, curvature, dv01 * 10000 / price, curvature / price)


def observation(name, unit, shock, start, exact, estimate):
    row = dict(case=name, shock_unit=unit, shock=shock, initial_price=start,
               exact=exact, linear=estimate.linear, curvature=estimate.curvature,
               second=estimate.total)
    for order in ('linear', 'second'):
        error = row[order] - exact
        row[order + '_signed_error'] = error
        row[order + '_abs_error'] = abs(error)
        row[order + '_error_pct'] = 100 * abs(error / exact) if exact else None
    return row


def bond_rows(years, coupon=0):
    y = 0.04
    if coupon:
        risk = coupon_risk(years, y, coupon)
        name = f'bond-{years}y-4pct-coupon'
    else:
        risk = zero_coupon_risk(1000, y, years)
        name = f'bond-{years}y-zero'
    for bp in range(-200, 201):
        new_y = y + bp / 10000
        price = zero_coupon_price(1000, new_y, years)
        price += sum(1000 * coupon / (1 + new_y)**t for t in range(1, years + 1))
        estimate = rates_pnl(risk.dv01, risk.dollar_convexity, bp)
        exact = price - risk.price if bp else 0.0
        yield observation(name, 'bp', bp, risk.price, exact, estimate)


def call_rows(name, years, strike=100, vol=0.20, shocks=None):
    args = (strike, 0.05, vol, years)
    spot = 100.0
    risk = black_scholes_call_risk(spot, *args)
    if shocks is None:
        shocks = (step / 10 for step in range(-200, 201))
    for percent in shocks:
        move = spot * percent / 100
        exact = black_scholes_call_price(spot + move, *args) - risk.price
        estimate = option_pnl(risk.delta, risk.gamma, move)
        yield observation(name, 'spot_pct', percent, risk.price, exact, estimate)


def experiments():
    for years in (2, 5, 10, 30):
        yield list(bond_rows(years))
    yield list(bond_rows(5, coupon=0.04))
    for name, years in [('1y', 1), ('30d', 30/365), ('7d', 7/365)]:
        yield list(call_rows('call-' + name, years))
    for strike in (90, 110):
        yield list(call_rows(f'call-1y-K{strike}', 1, strike=strike))
    for vol in (10, 40):
        yield list(call_rows(f'call-1y-vol{vol}', 1, vol=vol/100))


def crossings(rows):
    for sign in (-1, 1):
        outward = sorted((r for r in rows if r['shock'] * sign > 0),
                         key=lambda r: abs(r['shock']))
        for order in ('linear', 'second'):
            for tolerance in (1, 5):
                first = next((r['shock'] for r in outward
                              if r[order + '_error_pct'] > tolerance), None)
                yield dict(case=rows[0]['case'], unit=rows[0]['shock_unit'],
                           direction=sign, approximation=order, tolerance_pct=tolerance,
                           first_sample_above=first)


def scaled_calls():
    for name, years in [('1y', 1), ('30d', 30/365), ('7d', 7/365)]:
        for multiple in (-1, -.5, .5, 1):
            shock_pct = 100 * multiple * .2 * sqrt(years)
            row, = call_rows('call-' + name, years, shocks=[shock_pct])
            yield dict(row, vol_scale_multiple=multiple)


def write_csv(path, rows):
    rows = list(rows)
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    cases = list(experiments())
    output = Path('outputs')
    output.mkdir(exist_ok=True)
    write_csv(output / 'scenarios.csv', (row for case in cases for row in case))
    write_csv(output / 'crossings.csv', (row for case in cases for row in crossings(case)))
    write_csv(output / 'scaled-calls.csv', scaled_calls())
