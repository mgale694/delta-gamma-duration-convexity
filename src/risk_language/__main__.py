"""Run a compact exact-versus-approximate comparison."""

from __future__ import annotations

from .approximations import option_pnl, rates_pnl
from .models import (
    black_scholes_call_price,
    black_scholes_call_risk,
    zero_coupon_price,
    zero_coupon_risk,
)


def _row(
    instrument: str,
    shock: str,
    exact: float,
    linear: float,
    second_order: float,
) -> str:
    return (
        f"{instrument:<18} {shock:>10} {exact:>12.6f} "
        f"{linear:>12.6f} {second_order:>14.6f}"
    )


def main() -> None:
    option_inputs = {
        "spot": 100.0,
        "strike": 100.0,
        "rate": 0.05,
        "volatility": 0.20,
        "maturity": 1.0,
    }
    option_risk = black_scholes_call_risk(**option_inputs)

    bond_inputs = {
        "face": 1_000.0,
        "yield_rate": 0.04,
        "maturity": 5.0,
        "frequency": 1,
    }
    bond_risk = zero_coupon_risk(**bond_inputs)

    print(
        f"{'Instrument':<18} {'Shock':>10} {'Exact P&L':>12} "
        f"{'Linear':>12} {'Second order':>14}"
    )
    print("-" * 70)

    for spot_change in (-10.0, -2.0, 2.0, 10.0):
        exact = (
            black_scholes_call_price(
                **{**option_inputs, "spot": option_inputs["spot"] + spot_change}
            )
            - option_risk.price
        )
        approx = option_pnl(option_risk.delta, option_risk.gamma, spot_change)
        print(
            _row(
                "BS call",
                f"{spot_change:+.0f} spot",
                exact,
                approx.linear,
                approx.total,
            )
        )

    for yield_change_bp in (-100.0, -10.0, 10.0, 100.0):
        exact = (
            zero_coupon_price(
                **{
                    **bond_inputs,
                    "yield_rate": bond_inputs["yield_rate"]
                    + yield_change_bp / 10_000.0,
                }
            )
            - bond_risk.price
        )
        approx = rates_pnl(
            bond_risk.dv01,
            bond_risk.dollar_convexity,
            yield_change_bp,
        )
        print(
            _row(
                "Zero-coupon bond",
                f"{yield_change_bp:+.0f} bp",
                exact,
                approx.linear,
                approx.total,
            )
        )


if __name__ == "__main__":
    main()

