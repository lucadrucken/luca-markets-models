import numpy as np

from qp.portfolio import accrue_cash, rebalance_delta_hedge, hedge_portfolio_value


def test_accrue_cash_zero_rate():
    B0 = 100.0
    r = 0.0
    dt = 0.5
    assert accrue_cash(B0, r, dt) == B0


def test_accrue_cash_matches_exp():
    B0 = 100.0
    r = 0.05
    dt = 0.25
    expected = B0 * float(np.exp(r * dt))
    assert accrue_cash(B0, r, dt) == expected


def test_rebalance_delta_hedge_no_trade_no_cost():
    B0 = 50.0
    delta_old = 0.6
    delta_new = 0.6
    S = 100.0

    B1, cost, notional = rebalance_delta_hedge(B0, delta_old, delta_new, S, tc_per_dollar=0.001)

    assert B1 == B0
    assert cost == 0.0
    assert notional == 0.0


def test_rebalance_delta_hedge_trade_with_cost():
    B0 = 0.0
    delta_old = 0.5
    delta_new = 0.7
    S = 100.0
    tc = 0.001  # 10 bps

    traded_shares = delta_new - delta_old  # 0.2
    traded_notional = abs(traded_shares) * S  # 20
    expected_cost = tc * traded_notional  # 0.02
    expected_B1 = B0 - traded_shares * S - expected_cost  # -20.02

    B1, cost, notional = rebalance_delta_hedge(B0, delta_old, delta_new, S, tc_per_dollar=tc)

    assert B1 == expected_B1
    assert cost == expected_cost
    assert notional == traded_notional


def test_hedge_portfolio_value_short_option_example():
    # Example: short 1 option (qty=-1), delta=0.5, S=100, option=10, cash= -40
    # H = -10 + 0.5*100 - 40 = 0
    H = hedge_portfolio_value(option_value=10.0, option_qty=-1.0, delta=0.5, S=100.0, B=-40.0)
    assert H == 0.0
