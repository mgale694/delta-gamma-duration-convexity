# How local is a frozen sensitivity?

## Reproduction

From the repository root run `make test evidence` with Python 3.9 or later. The calculations use the standard library. To render the two PNG figures run `make figures` with Matplotlib installed in the active Python environment (tested with 3.11.2). Generated files are written to `outputs/`. All scenario inputs are synthetic. No price history, calibration or data download is needed.

## Design

For each instrument, compute the base price and risk once, then move a single factor and reprice the same cash flows or payoff under the same model. Each row is an independent shock from the same base. The scenarios are instantaneous. A seven-day expiry specifies remaining time in both valuations.

| Family | Base case and controls | Symmetric grid |
| --- | --- | --- |
| Bonds | 1,000 face, 4% nominal annual yield, annual compounding. Zero coupons at 2, 5, 10 and 30 years. Five-year 4% annual coupon on a coupon date, first coupon in one year. | −200 to +200 bp in 1 bp steps |
| European calls | Per share, spot and strike 100, 5% continuously compounded rate, volatility 20%, zero dividends. Expiries of 1 year, 30/365 and 7/365 years. One-year variants change only the strike (90 or 110) or volatility (10% or 40%). | −20% to +20% spot in 0.1 percentage point steps |
| Expiry control | ATM calls with the same three expiries. Shock the spot by a fraction of its initial value equal to ±0.5 or ±1 times annual volatility times the square root of years remaining. | Four shocks per expiry |

The expiry control uses arithmetic spot moves scaled by log-return volatility. This is a comparison of scales. It assigns no forecast probability to a move and does not equate return distributions across maturities.

## Measurements

* `scenarios.csv` contains 12 cases × 401 rows, including 12 zero controls. Currency values are per bond or per share. The illustrations use sterling. Signed error is estimate minus model-repriced P&L. Absolute percentage error divides absolute cash error by absolute model P&L. At zero P&L the percentage is blank. Near zero a small cash error can yield a large percentage.
* `crossings.csv` gives the first sampled move strictly above an illustrative 1% or 5% error on each side, walking outwards from zero. Blank means no breach was observed within the grid. A first breach gives the end of the contiguous sampled acceptable region on that side. Later points can return below the threshold. Neither tolerance is an industry convention.
* `scaled-calls.csv` holds the 12 expiry-control valuations and their volatility multiples.
* `bond-and-call.png` shows baseline P&L above relative error. `expiry-stress.png` compares one year and one week on common spot and P&L scales.

## Why the residual changes

With decimal yield y and annual compounding, a zero paying F in n years costs F/(1+y)^n. Its first derivative is −nP/(1+y) and its second is n(n+1)P/(1+y)^2. The third derivative is negative, −n(n+1)(n+2)P/(1+y)^3. Therefore the tangent underestimates price on either side, while the quadratic overestimates price for a yield rise and underestimates it for a fall. Cash flows of the coupon bond can be differentiated separately and summed.

Modified duration is −P′/P. Our analytic DV01 is −P′ × 0.0001 in currency per basis point. Thus a signed shock of b bp produces linear P&L of −DV01 × b. The second-order term is 0.5 × P″ × (b/10,000)². The option uses a currency spot move, giving delta × ΔS + 0.5 × gamma × ΔS².

For a smooth price, Taylor's theorem puts the quadratic residual at the third derivative somewhere along the move times the signed move cubed divided by six. More intuitively, the exact change in value is the accumulated slope along the move. The quadratic estimates that change by letting slope evolve at its initial rate. For a call approaching expiry, gamma can be concentrated into a narrow range around the strike. The extrapolated quadratic then keeps bending far outside that range. For a positive spot bump the true price gain of this European call is bounded by the bump (delta is between zero and one). For a negative bump the price cannot increase. Check either condition to catch an implausible estimate before measuring the error.

Near the origin, where the starting slope is nonzero and the leading residual coefficients do not vanish, first- and second-order cash errors typically scale as the squared and cubed move. Dividing by approximately linear exact P&L reduces those powers by one. Those rates describe local behaviour. Currency errors and normalised errors answer different questions, especially for heavily out-of-the-money options.

## Validation and boundaries

The suite checks baseline benchmarks, analytical Greeks against centred bumps, coupon-strip valuation against the annuity formula, and DV01 against a symmetric one-basis-point bump. A separate discounted-payoff integration checks one-year and seven-day call prices at five spots including both stress endpoints. Zero, sign, convexity, missing-ratio and first-crossing checks exercise the generated data. Repricing is exact within the selected pricing model. Volatility, rates, time, cash flows and other risk factors stay fixed. A yield shock here acts on a single yield to maturity. Live P&L, curve twists, transaction costs and hedge rebalancing are outside this experiment.

## References

* The effect of compounding, cash-flow timing and convexity on yield-based risk. CFA Institute, 2026 Level I curriculum, [Yield-Based Bond Convexity and Portfolio Properties](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).
* Analytic modified-duration and finite-bump approaches to DV01. CME Group, [Calculating the Dollar Value of a Basis Point](https://www.cmegroup.com/trading/interest-rates/files/Calculating_the_Dollar_Value_of_a_Basis_Point.pdf).
* European option model and assumptions. Black and Scholes (1973), [The Pricing of Options and Corporate Liabilities](https://doi.org/10.1086/260062).
* Dependence of gamma on moneyness, expiry and volatility. Options Industry Council, [Gamma](https://www.optionseducation.org/advancedconcepts/gamma).
* Smoothness requirements and the evaluation point of the next derivative. OpenStax, Calculus Volume 2, §6.3, [Taylor’s theorem with remainder](https://openstax.org/books/calculus-volume-2/pages/6-3-taylor-and-maclaurin-series).

Sources consulted 18 November 2026. The scenario outputs and selected cutoffs are this project's calculations.
