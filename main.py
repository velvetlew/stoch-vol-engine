from products.european_call import EuropeanCall

ec1 = EuropeanCall(100, 100, 0.05, 1, 0.2, 0.1)
print(ec1.payoff(110))  # Output: 10
print(ec1.S)

print(ec1.type)