import numpy as np
import matplotlib.pyplot as plt

from products.european_call import EuropeanCall
from models.black_scholes import BlackScholes
from models.heston import Heston


def main():
    # Basic parameters
    spot = 100
    maturity = 1
    risk_free_rate = 0.05
    dividend_yield = 0.02
    volatility = 0.25

    # Heston-specific parameters
    reversion_level = 0.30
    reversion_rate = 1.50
    vol_of_vol = 0.40
    correlation = -0.70

    # Compare prices across different strike prices
    strikes = np.linspace(60, 180, 30)

    bs_prices = []
    heston_prices = []

    bs_model = BlackScholes()

    for strike in strikes:
        # Black-Scholes model uses EuropeanCall object
        option = EuropeanCall(
            spot,
            strike,
            risk_free_rate,
            maturity,
            volatility,
            dividend_yield,
        )

        bs_price = bs_model.get_price(option)
        bs_prices.append(bs_price)

        # Heston model
        heston_model = Heston(
            spot=spot,
            strike=strike,
            maturity=maturity,
            risk_free_rate=risk_free_rate,
            dividend_yield=dividend_yield,
            type="call",
            volatility=volatility,
            reversion_level=reversion_level,
            reversion_rate=reversion_rate,
            vol_of_vol=vol_of_vol,
            correlation=correlation,
        )

        heston_price = heston_model.get_price()
        heston_prices.append(heston_price)

    # Print comparison table
    print("Strike | Black-Scholes | Heston")
    print("--------------------------------")
    for strike, bs_price, heston_price in zip(strikes, bs_prices, heston_prices):
        print(f"{strike:6.2f} | {bs_price:13.4f} | {heston_price:8.4f}")

    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.plot(strikes, bs_prices, marker="o", label="Black-Scholes")
    plt.plot(strikes, heston_prices, marker="s", label="Heston")

    plt.title("Option Price Comparison: Black-Scholes vs Heston")
    plt.xlabel("Strike Price")
    plt.ylabel("Call Option Price")
    plt.legend()
    plt.grid(True)

    plt.savefig("bs_vs_heston.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
