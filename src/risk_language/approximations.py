"""Second-order P&L approximations with explicit market conventions."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class PnLBreakdown:
    """Linear and curvature contributions to an approximate price change."""

    linear: float
    curvature: float

    @property
    def total(self) -> float:
        return self.linear + self.curvature


def _require_finite(**values: float) -> None:
    for name, value in values.items():
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")


def option_pnl(delta: float, gamma: float, spot_change: float) -> PnLBreakdown:
    """Approximate option P&L for a spot move in currency units.

    ``delta`` has units of option-price currency per unit of spot currency.
    ``gamma`` has units of option-price currency per squared spot unit.
    """

    _require_finite(delta=delta, gamma=gamma, spot_change=spot_change)
    return PnLBreakdown(
        linear=delta * spot_change,
        curvature=0.5 * gamma * spot_change**2,
    )


def rates_pnl(
    dv01: float,
    dollar_convexity: float,
    yield_change_bp: float,
) -> PnLBreakdown:
    """Approximate bond P&L for a parallel yield move in basis points.

    The convention is a non-negative DV01 loss magnitude: the linear P&L of
    a conventional long bond is ``-dv01 * yield_change_bp``. Dollar convexity
    is the second derivative of price with respect to *decimal* yield.
    """

    _require_finite(
        dv01=dv01,
        dollar_convexity=dollar_convexity,
        yield_change_bp=yield_change_bp,
    )
    if dv01 < 0:
        raise ValueError("dv01 must be a non-negative loss magnitude")

    decimal_yield_change = yield_change_bp / 10_000.0
    return PnLBreakdown(
        linear=-dv01 * yield_change_bp,
        curvature=0.5 * dollar_convexity * decimal_yield_change**2,
    )

