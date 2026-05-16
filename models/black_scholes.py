class BlackScholes:

    def __init__ (self):
        pass

    def get_price(self, option):
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