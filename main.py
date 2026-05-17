from products.european_call import EuropeanCall

from models.black_scholes import BlackScholes
from models.heston import Heston

ec1 = EuropeanCall(100, 100, 0.05, 1, 0.2, 0.1)
print(ec1.payoff(110))  # Output: 10
print(ec1.S)

print(ec1.type)

model = Heston(spot=50, strike=50, maturity=1, risk_free_rate=0.05, dividend_yield=0.02, type="call", volatility=0.25, reversion_level=0.3, reversion_rate=0.05, vol_of_vol=2, correlation=-0.5)


price = model.get_price()

print(price)