"""Small analytic models used to test the risk approximations."""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, log, pi, sqrt


@dataclass(frozen=True)
class OptionRisk:
    price: float
    delta: float
    gamma: float


@dataclass(frozen=True)
class RatesRisk:
    price: float
    dv01: float
    dollar_convexity: float
    modified_duration: float
    convexity: float


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def _normal_pdf(value: float) -> float:
    return exp(-0.5 * value**2) / sqrt(2.0 * pi)


def _validate_option_inputs(
    spot: float,
    strike: float,
    volatility: float,
    maturity: float,
) -> None:
    if spot <= 0:
        raise ValueError("spot must be positive")
    if strike <= 0:
        raise ValueError("strike must be positive")
    if volatility <= 0:
        raise ValueError("volatility must be positive")
    if maturity <= 0:
        raise ValueError("maturity must be positive")


def black_scholes_call_risk(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
) -> OptionRisk:
    """Return Black–Scholes call price, delta, and gamma.

    ``rate`` and ``volatility`` are decimals and ``maturity`` is in years.
    The model assumes no dividends.
    """

    _validate_option_inputs(spot, strike, volatility, maturity)
    root_time = sqrt(maturity)
    d1 = (
        log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * root_time)
    d2 = d1 - volatility * root_time
    discount = exp(-rate * maturity)

    return OptionRisk(
        price=spot * _normal_cdf(d1) - strike * discount * _normal_cdf(d2),
        delta=_normal_cdf(d1),
        gamma=_normal_pdf(d1) / (spot * volatility * root_time),
    )


def black_scholes_call_price(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
) -> float:
    return black_scholes_call_risk(
        spot, strike, rate, volatility, maturity
    ).price


def _validate_bond_inputs(
    face: float,
    yield_rate: float,
    maturity: float,
    frequency: int,
) -> None:
    if face <= 0:
        raise ValueError("face must be positive")
    if maturity <= 0:
        raise ValueError("maturity must be positive")
    if frequency <= 0:
        raise ValueError("frequency must be a positive integer")
    if 1.0 + yield_rate / frequency <= 0:
        raise ValueError("yield is outside the model domain")


def zero_coupon_price(
    face: float,
    yield_rate: float,
    maturity: float,
    frequency: int = 1,
) -> float:
    """Price a zero-coupon bond at a nominal compounded annual yield."""

    _validate_bond_inputs(face, yield_rate, maturity, frequency)
    return face * (1.0 + yield_rate / frequency) ** (-frequency * maturity)


def zero_coupon_risk(
    face: float,
    yield_rate: float,
    maturity: float,
    frequency: int = 1,
) -> RatesRisk:
    """Return analytic price, DV01, duration, and convexity for a zero.

    DV01 is returned as a positive magnitude per basis point. Dollar convexity
    is the second price derivative per squared unit of decimal yield.
    """

    price = zero_coupon_price(face, yield_rate, maturity, frequency)
    yield_base = 1.0 + yield_rate / frequency
    modified_duration = maturity / yield_base
    convexity = maturity * (maturity + 1.0 / frequency) / yield_base**2
    return RatesRisk(
        price=price,
        dv01=modified_duration * price / 10_000.0,
        dollar_convexity=convexity * price,
        modified_duration=modified_duration,
        convexity=convexity,
    )

