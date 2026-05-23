class BlackScholes:

    def __init__ (self):
        pass

    def get_price(self, option):

        """Compute the Black-Scholes price for a European option.

        Parameters
        ----------
        option : object
            An option object with the attributes:
            - S: spot price
            - K: strike price
            - T: time to maturity (in years)
            - r: risk-free interest rate
            - sigma: volatility
            - q: continuous dividend yield
            - type: 'call' or 'put'

        Returns
        -------
        float
            The Black-Scholes price for the given option.

        Raises
        ------
        ValueError
            If the option type is not 'call' or 'put'.
        """
        
        from scipy.stats import norm
        import numpy as np

        S = option.S
        K = option.K
        T = option.T
        r = option.r
        sigma = option.sigma
        q = option.q

        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option.type == 'call':
            price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option.type == 'put':
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        else:
            raise ValueError("Option type must be 'call' or 'put'")

        return price