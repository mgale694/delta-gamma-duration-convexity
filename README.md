# Delta, Gamma, Duration and Convexity

## A Common Language for Non-Linear Financial Risk

This repository is the public, reproducible evidence base for a research project comparing local risk measures in options and rates.

The central idea is simple: both markets use a first-order sensitivity plus a second-order curvature term. The details matter, though—state variables, units, scaling, and sign conventions are not interchangeable.

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

```
make example
make test
```

The example prints exact repricing alongside linear and second-order estimates for a Black–Scholes call and a zero-coupon bond.

For development environments with a current pip, an editable install also exposes the `risk-language` command:

```
python3 -m pip install -e .
risk-language
```

## Repository map

```
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

Foundation scaffold complete. The next research milestone is to lock representative instrument parameters, generate error curves over shock size, and promote validated results into the article.

## Contributing

Issues and focused pull requests are welcome. Please state units and sign conventions explicitly, add tests for new calculations, and avoid committing generated artifacts that cannot be reproduced.

## License

No license has been selected yet. Until one is added, copyright remains with the repository owner and reuse is not granted by default.
