# Methodology and Conventions

## Generic local approximation

For a twice-differentiable value $V(x)$, the second-order Taylor approximation around $x$ is

$
V(x + \Delta x) - V(x)
\approx V'(x)\Delta x + \frac{1}{2}V''(x)(\Delta x)^2.
$

It is local: the sensitivities are measured at the starting point and other state variables are assumed fixed.

## Options

For spot $S$:

$
\Delta V \approx \Delta\,\Delta S + \frac{1}{2}\Gamma(\Delta S)^2,
$

where

$
\Delta = \frac{\partial V}{\partial S}, \qquad
\Gamma = \frac{\partial^2 V}{\partial S^2}.
$

If price and spot use the same currency, delta is currency per spot-currency unit and gamma is currency per squared spot-currency unit. The included reference model is a non-dividend-paying European call under Black–Scholes; it isolates spot sensitivity and holds rate, volatility, and time fixed during each repricing.

## Rates

For yield $y$, expressed as a decimal:

$$
\Delta P \approx \frac{\partial P}{\partial y}\Delta y
+ \frac{1}{2}\frac{\partial^2 P}{\partial y^2}(\Delta y)^2.
$$

This project uses:

$$
DV01 = -\frac{\partial P}{\partial y}\times 10^{-4},
\qquad
C_\$ = \frac{\partial^2 P}{\partial y^2}.
$$

For a yield shock $b$ expressed in basis points, $\Delta y=b/10{,}000$, so

$$
\Delta P \approx -DV01\,b
+ \frac{1}{2}C_\$\left(\frac{b}{10{,}000}\right)^2.
$$

DV01 is therefore a non-negative loss magnitude for a conventional long bond when yield rises by one basis point. Some systems instead store a signed first derivative or PV01 with a desk-specific sign. Those values must be normalized before using the formula in this repo.

Normalized convexity is

$$
C = \frac{1}{P}\frac{\partial^2P}{\partial y^2},
$$

so dollar convexity is $C_\$=P C$. Mixing these two is a dimensional error.

## Reference instruments

The code uses deliberately small analytic models:

- a European call under Black–Scholes, with no dividends;
- a zero-coupon bond under nominal periodic compounding.

They are teaching and verification instruments, not production pricing models. Their closed-form sensitivities let tests focus on the approximation rather than numerical infrastructure.

## What the analogy does not imply

- Delta and DV01 act on different state variables and use different conventional shock units.
- Delta is naturally signed; DV01 is often reported as a positive magnitude.
- Gamma and bond convexity can have different signs for instruments with embedded features.
- Real P&L also reflects volatility, curve shape, time, carry, cross-effects, and model changes.
- A second-order approximation is not exact revaluation, particularly for large shocks or discontinuous payoffs.

## Reproducibility rule

Every published numerical result should identify its input parameters, the exact repricing function, the approximation convention, and the code version. Generated tables and figures belong in `outputs/` and must be reproducible by a checked-in command.

