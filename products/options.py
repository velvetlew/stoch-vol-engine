class Option:
    """
    Class for options pricing and Greeks calculations. \n

    Parameters
    """

    def __init__ (self, spot, strike, maturity, risk_free_rate, volatility, dividend_yield, type):
        self.S = spot
        self.K = strike
        self.T = maturity
        self.r = risk_free_rate
        self.sigma = volatility
        self.q = dividend_yield
        self.type = type