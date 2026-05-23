import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# from products.european_call import EuropeanCall

class HestonMonteCarlo:

    def __init__ (self):
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
