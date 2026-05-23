from products.options import Option
import numpy as np

class EuropeanCall(Option):
    """European call option product.

    Inherits from the generic Option base class and implements the payoff for
    a European-style call option.
    """
    
    def __init__(self, spot, strike, maturity, risk_free_rate, volatility, dividend_yield):
        """Initialize a European call option.

        Parameters:
            spot: Current underlying asset price.
            strike: Option strike price.
            maturity: Time to expiration.
            risk_free_rate: Constant risk-free interest rate.
            volatility: Annualized asset volatility.
            dividend_yield: Continuous dividend yield.
        """
        super().__init__(spot, strike, maturity, risk_free_rate, volatility, dividend_yield, type='call')
        
    def payoff(self, S):
        """Calculate the payoff of the call option at maturity.

        Parameters:
            S: Terminal underlying asset price.

        Returns:
            np.ndarray or float: Payoff value max(S - K, 0).
        """
        return np.maximum(S - self.K, 0)