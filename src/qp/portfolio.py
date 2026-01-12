import numpy as np
from typing import Tuple

def accrue_cash(B: float, r: float, dt: float) -> float:
    return B * float(np.exp(r * dt))

def rebalance_delta_hedge(
    B: float,
    delta_old: float,
    delta_new: float,
    S: float,
    tc_per_dollar: float = 0.0
) -> Tuple[float, float, float]:
    """
    Rebalance stock position from delta_old to delta_new at price S.

    Transaction costs are modeled as: cost = tc_per_dollar * |traded_notional|.
    Returns updated cash, cost paid, and traded notional.
    """
    traded_shares = delta_new - delta_old
    traded_notional = abs(traded_shares) * S
    cost = tc_per_dollar * traded_notional
    B_new = B - traded_shares * S - cost
    return float(B_new), float(cost), float(traded_notional)

def hedge_portfolio_value(option_value: float, option_qty: float, delta: float, 
                          S: float, B: float) -> float:
    return option_qty * option_value + delta * S + B


