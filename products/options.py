class Option:
    """Base option class for European-style option products.

    This class stores core option parameters used by pricing models and
    payoff implementations.
    """

    def __init__ (self, spot, strike, maturity, risk_free_rate, volatility, dividend_yield, type):
        """Initialize an option with standard inputs.

        Parameters:
            spot: Current underlying asset price.
            strike: Option strike price.
            maturity: Time to expiration.
            risk_free_rate: Continuously compounded risk-free interest rate.
            volatility: Annualized volatility of the underlying.
            dividend_yield: Continuous dividend yield.
            type: Option type label, usually 'call' or 'put'.
        """
        self.S = spot
        self.K = strike
        self.T = maturity
        self.r = risk_free_rate
        self.sigma = volatility
        self.q = dividend_yield
        self.type = type