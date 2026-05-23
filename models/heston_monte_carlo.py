import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# from products.european_call import EuropeanCall

class HestonMonteCarlo:
    """Monte Carlo pricing engine for the Heston stochastic volatility model.

    This class generates spot and variance paths for an underlying asset under
    Heston dynamics and computes option prices by discounting expected payoffs.

    Methods:
        get_price: Price a European option using Monte Carlo simulation.
        get_simulation: Simulate asset and variance paths under Heston dynamics.
        plot_st: Plot the distribution of asset prices at maturity.
    """

    def __init__(self):
        """Initialize the Heston Monte Carlo engine."""
        pass
    
    def get_price(
            self, 
            option,
            reversion_level,
            reversion_rate,
            vol_of_vol,
            correlation,
            num_of_steps, 
            num_of_sim
        ):
        """Compute the discounted Monte Carlo price of a European option.

        Parameters:
            option: Option object with attributes S, K, r, T, sigma, and type.
            reversion_level: Long-run variance level (theta) for the Heston model.
            reversion_rate: Speed of mean reversion (kappa).
            vol_of_vol: Volatility of volatility (xi).
            correlation: Correlation between asset and variance Brownian motions.
            num_of_steps: Number of time steps in the simulation.
            num_of_sim: Number of Monte Carlo sample paths.

        Returns:
            float: Discounted expected payoff of the option.
        """

        # sim = self.get_simulation(option, reversion_level, reversion_rate, vol_of_vol, correlation, num_of_steps, num_of_sim)

        ST = self.get_simulation(option, reversion_level, reversion_rate, vol_of_vol, correlation, num_of_steps, num_of_sim)[0][-1]
        K = option.K
        r = option.r
        T = option.T
        type = option.type

        if type == "call":
            payoff = np.maximum(ST - K, 0.0)
        else:
            payoff = np.maximum(K - ST, 0.0)

        return np.exp(-r * T) * np.mean(payoff)

    def get_simulation(
            self, 
            option,
            reversion_level,
            reversion_rate,
            vol_of_vol,
            correlation,
            num_of_steps, 
            num_of_sim
        ):
        """Simulate paths for the underlying asset and variance process.

        The simulation uses the Heston model discretization with correlated
        Brownian increments for the asset and variance processes.

        Parameters:
            option: Option object providing initial spot S, rate r, maturity T,
                and initial volatility sigma.
            reversion_level: Long-run variance level (theta).
            reversion_rate: Mean reversion speed (kappa).
            vol_of_vol: Volatility of volatility (xi).
            correlation: Correlation between asset and variance increments.
            num_of_steps: Number of time steps in the simulation.
            num_of_sim: Number of Monte Carlo sample paths.

        Returns:
            tuple: (S_paths, v_paths) arrays of shape (num_of_steps+1, num_of_sim).
        """

        s0=option.S
        r=option.r
        T=option.T
        v0=option.sigma ** 2
        
        dt = float(T / num_of_steps)
        
        theta = float(reversion_level ** 2)
        kappa = float(reversion_rate)
        xi = float(vol_of_vol)
        rho = float(correlation)

        # Drift vector
        mu = np.array([0, 0])

        # Correlation matrix
        cov = np.array([[1, rho], [rho, 1]])


        # arrays for storing prices and variances
        self.S = np.full(shape=(num_of_steps+1,num_of_sim), fill_value=s0, dtype=float)
        self.v = np.full(shape=(num_of_steps+1,num_of_sim), fill_value=v0, dtype=float)

        Z = np.random.multivariate_normal(mu, cov, (num_of_steps, num_of_sim))

        # simulate paths
        for i in range(1,num_of_steps+1):
            self.S[i] = self.S[i-1] * np.exp( (r - 0.5*self.v[i-1])*dt + np.sqrt(self.v[i-1] * dt) * Z[i-1,:,0] )
            self.v[i] = np.maximum(self.v[i-1] + kappa*(theta-self.v[i-1])*dt + xi*np.sqrt(self.v[i-1]*dt)*Z[i-1,:,1],0)
        
        return self.S, self.v

    def plot_st(
            self, 
            option,
            reversion_level,
            reversion_rate,
            vol_of_vol,
            correlation,
            num_of_steps, 
            num_of_sim
        ):
        """Plot the density of simulated asset prices at maturity.

        Parameters:
            option: Option object with initial asset and model parameters.
            reversion_level: Long-run variance level (theta).
            reversion_rate: Mean reversion speed (kappa).
            vol_of_vol: Volatility of volatility (xi).
            correlation: Correlation between asset and variance increments.
            num_of_steps: Number of time steps in the simulation.
            num_of_sim: Number of Monte Carlo sample paths.

        Returns:
            np.ndarray: Simulated terminal asset prices S_T.
        """

        ST = self.get_simulation(option, reversion_level, reversion_rate, vol_of_vol, correlation, num_of_steps, num_of_sim)[0][-1]
        
        theta = float(reversion_level ** 2)
        kappa = float(reversion_rate)
        xi = float(vol_of_vol)
        rho = float(correlation)

        fig, ax = plt.subplots()

        ax = sns.kdeplot(ST, ax=ax)
        # ax = sns.kdeplot(gbm, label="GBM", ax=ax)
        S_min = ST.min()
        S_max = ST.max()

        plt.title(r'Asset Price at Maturity $\kappa$=%.2f, $\theta$=%.2f, $\xi$=%.2f, $\rho$=%.2f' % (kappa, theta, xi, rho))
        plt.xlim([S_min, S_max])
        plt.xlabel('$S_T$')
        plt.ylabel('Density')
        plt.legend()
        plt.show()

        return ST

# p = model.get_simulation(option=EuropeanCall(spot=100, strike=100, risk_free_rate=0.05, maturity=1, volatility=0.2, dividend_yield=0), reversion_level=0.3, reversion_rate=3, vol_of_vol=0.6, correlation=-0.5, num_of_steps=252, num_of_sim=10000)
# S_sim, V_sim = model.get_simulation(option=EuropeanCall(100, 100, 0.05, 1, 0.2, 0.1), reversion_level=0.3, reversion_rate=0.05, vol_of_vol=2, correlation=-0.5, num_of_steps=252, num_of_sim=1000)
