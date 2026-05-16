from products.options import Option
import numpy as np

class EuropeanPut(Option):

    def __init__ (self, spot, strike, maturity, risk_free_rate, volatility, dividend_yield):
        super().__init__(spot, strike, maturity, risk_free_rate, volatility, dividend_yield, type='put')

    def payoff(self, S):
        return np.maximum(self.K - S, 0)