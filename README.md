# Delta, Gamma, Duration and Convexity

## A Common Language for Non-Linear Financial Risk

This repository is the public, reproducible evidence base for a research project investigating how local risk measures behave as the market moves away from the point at which those measures were calculated.

The common mathematical structure is the starting point: options use delta and gamma to describe local slope and curvature, while rates use duration/DV01 and convexity. The more interesting question is **how far those local approximations can be pushed before they stop providing a reliable estimate of actual P&L, and how much the second-order term improves that estimate**.

## Research question

How reliable are first-order risk measures as the underlying market moves, and how much does second-order curvature improve the approximation?

The project uses bonds and options as two controlled examples of the same general problem:

- compare exact repricing with a first-order approximation;
- add the second-order term and measure the improvement;
- examine how approximation error changes as the shock grows;
- make clear where the analogy between the two markets is useful, and where differences in state variables, units, scaling, and sign conventions matter.

The goal is not to show that duration/convexity and delta/gamma are interchangeable. It is to use them to study a broader idea: **risk measures are local descriptions of nonlinear pricing functions**.

## The common structure

For a value function $(V(x))$, a small move $(\Delta x)$ gives

$$
\Delta V \approx \frac{\partial V}{\partial x}\Delta x
+ \frac{1}{2}\frac{\partial^2 V}{\partial x^2}(\Delta x)^2.
$$

| Market | State move | Linear term | Curvature term |
| --- | --- | --- | --- |
| Options | Spot move $\Delta S$ | $\Delta\,\Delta S$ | $\frac{1}{2}\Gamma(\Delta S)^2$ |
| Rates | Yield move $b$ in bp | $-DV01\,b$ | $\frac{1}{2}\,C_\$\,(b/10{,}000)^2$ |

This repo quotes **DV01 as a positive loss magnitude for a +1 bp yield move** on a conventional long bond. $C_\$$ is dollar convexity, the second derivative of price with respect to decimal yield. See [the methodology](docs/methodology.md) for definitions and caveats.

## Quick start

Python 3.9 or later is sufficient; the library has no runtime dependencies. Run the example and tests directly from a clean checkout:

```bash
make example
make test
```

The example prints exact repricing alongside linear and second-order estimates for a Black–Scholes call and a zero-coupon bond.

For development environments with a current pip, an editable install also exposes the `risk-language` command:

```bash
python3 -m pip install -e .
risk-language
```

## Repository map

```text
src/risk_language/   Transparent reference implementations
tests/               Unit and approximation checks
docs/                Definitions, conventions, and methodology
data/                Provenance notes for any future external data
outputs/             Reproducible generated artifacts only
```

## Source-of-truth boundary

- **This repo:** canonical maths, code, tests, numerical results, and generated figures
- **Private Project Studio:** research log, editorial decisions, scripts, and publishing workflow
- **Atlas:** final edited research article

The public repo should make every technical claim in the article or video independently inspectable. It should not become a mirror of editorial drafts.

## Status

Foundation scaffold complete. The next research milestone is to lock representative instrument parameters, generate exact-versus-approximate P&L and error curves over shock size, and determine where first-order approximations begin to deteriorate materially and how much second-order terms repair that error.

Validated conclusions can then be promoted into the Atlas article and used selectively in the simpler long-form video.

## Contributing

Issues and focused pull requests are welcome. Please state units and sign conventions explicitly, add tests for new calculations, and avoid committing generated artifacts that cannot be reproduced.

## License

No license has been selected yet. Until one is added, copyright remains with the repository owner and reuse is not granted by default.
