# Luca Markets Models – Derivatives, Hedging & Risk

_Luca Druckenmüller_

This repository contains quantitative finance tools and notebooks focused on **derivatives pricing, hedging strategies and risk analysis** in a global markets and trading desk context.


Main focus:
- Discrete delta hedging of European options (including transaction costs & model risk)
- Option pricing (Black–Scholes, Binomial)
- Fixed income analytics (duration, convexity)
- Risk & performance metrics (VaR, ES, Sharpe)

---

## Installation

```bash
git clone https://github.com/lucadrucken/luca-markets-models.git
cd luca-markets-models
pip install -r requirements.txt
# installs qp as well because of '-e .' → all models available via top-level imports
```

---

## Quickstart

### Delta Hedging – Discrete Replication of a Sold European Call

The notebook `01_delta_hedging.ipynb` simulates the discrete delta hedging of a short European call option under Black–Scholes.

It analyzes:
- Daily vs. weekly rebalancing
- Volatility mis-specification (model risk)
- Transaction costs
- Distribution of terminal hedging error (VaR, ES, MSHE)

Key outputs:
- Underlying GBM paths
- Option value vs. hedging portfolio value
- Hedging error distributions
- Risk vs. cost trade-offs


### Performance

```python
from qp import sharpe
import numpy as np

returns = np.array([0.001, -0.0005, 0.0008, 0.0012, -0.0009, 0.0004, 0.0015])

rf_annual = 0.02
rf_daily = rf_annual / 252

sr = sharpe(returns, risk_free=rf_daily, periods_per_year=252)
print(f"Annualized Sharpe = {sr:.2f}")
```

### Risk

```python
from qp import var_historical
import numpy as np

returns = np.array([0.004, -0.006, 0.001, -0.012, 0.003, 0.007, -0.004, 0.002])

var99 = var_historical(returns, level=0.99)
print(f"VaR(99%) per period = {var99:.4f}")
```

### Bond Pricing

```python
from qp import bond_price

price = bond_price(face_value=1000, maturity=5,
                   coupon_rate=0.05, ytm=0.04, freq=2)
print(price)  # -> ~1035.74
```

### Black–Scholes (European Options)

```python
from qp import bs_price

call = bs_price(100, 100, 0.02, 0.01, 0.2, 1.0, "call")
put  = bs_price(100, 100, 0.02, 0.01, 0.2, 1.0, "put")
print(call, put)
```

### Binomial Model (European & American)

```python
from qp import binomial_price

eu_put = binomial_price(100, 100, 0.05, 0.0, 0.2, 1.0,
                        steps=500, option_type="put", american=False)
am_put = binomial_price(100, 100, 0.05, 0.0, 0.2, 1.0,
                        steps=500, option_type="put", american=True)
print(eu_put, am_put)  # American Put >= European Put
```

---

## Tests

All models are covered by unit tests using Pytest:

```bash
pip install pytest
pytest -q
```

---

## Available Functions

### Risk
- `var_historical(returns, level)` – Historical Value-at-Risk
- `es_historical(returns, level)` – Historical Expected Shortfall

### Performance
- `sharpe(returns, risk_free, periods_per_year)` – Annualized Sharpe Ratio

### Portfolio (Hedging)
- `accrue_cash(B, r, dt)` – Accrues the cash account at the risk-free rate
- `rebalance_delta_hedge(B, delta_old, delta_new, S, tc_per_dollar=0.0)` – Executes delta hedge rebalancing including transaction costs
- `hedge_portfolio_value(option_value, option_qty, delta, S, B)` – Computes the value of the self-financing hedging portfolio

### Fixed Income
- `bond_price(face_value, maturity, coupon_rate, ytm, freq)` – Price of a fixed coupon bond
- `macaulay_duration(...)` – Weighted average time to receive cashflows
- `modified_duration(...)` – Interest rate sensitivity (Macaulay adjusted by yield)
- `dollar_duration(...)` – Price change per 1 bp change in yield
- `convexity(...)` – Curvature of price–yield relationship (second-order sensitivity)

### Derivatives
- `bs_price(S, K, r, q, sigma, T, option_type)` – Black–Scholes price
- `binomial_price(...)` – Binomial pricing (European/American)
- `bs_greeks(...)` – Black–Scholes Greeks
- `call_from_put(...)`, `put_from_call(...)` – Put–Call parity helpers
- `parity_gap(...)`, `parity_bounds(...)` – Put–Call parity diagnostics



## Project Structure

```
LUCA-MARKETS-MODELS/
├── notebooks/                   
│   └── 01_delta_hedging.ipynb   # delta hedging of sold european call
│  
├── src/qp/                      # main package (all models)
│   ├── __init__.py
│   ├── derivatives.py           
│   ├── fixed_income.py          
│   ├── performance.py           
│   ├── portfolio.py             
│   └── risk.py                  
│
├── tests/                       # pytest unit tests
│  
├── requirements.txt             # dependencies
├── pyproject.toml               
├── README.md
└── .gitignore
```
