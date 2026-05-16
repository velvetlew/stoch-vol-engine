from products.options import Option
import numpy as np

class EuropeanCall(Option):
    
    def __init__ (self, spot, strike, maturity, risk_free_rate, volatility, dividend_yield):
        super().__init__(spot, strike, maturity, risk_free_rate, volatility, dividend_yield, type='call')
        
    def payoff(self, S):
        return np.maximum(S - self.K, 0)