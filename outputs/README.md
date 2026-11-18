# Article evidence

| File | Contents |
| --- | --- |
| [scenarios.csv](scenarios.csv) | 4,812 base and shocked valuations across 12 instrument configurations |
| [crossings.csv](crossings.csv) | First sampled breaches of the 1% and 5% P&L error budgets, by direction |
| [scaled-calls.csv](scaled-calls.csv) | 12 spot shocks scaled to the volatility and remaining time of each call |
| [bond-and-call.png](bond-and-call.png) | Baseline P&L and error curves for a five-year bond and one-year call |
| [expiry-stress.png](expiry-stress.png) | A one-year and a seven-day call on the same axes |

Run `make evidence` for the CSVs or `make figures` for CSVs and plots. The committed review snapshot uses Python 3.9.6 for the sweep and Matplotlib 3.11.2 for plotting. Numerical rounding and rasterisation can vary slightly across runtime versions. The [experiment design](../docs/experiments.md) defines each field and scenario.
