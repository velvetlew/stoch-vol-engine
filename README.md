# Stoch-Vol-Engine

## Project description
A compact implementation of stochastic volatility option pricing using the Heston model. The project compares Black-Scholes and Heston pricing, and includes notebook output conversion for report generation.

## Project structure
```
stoch-vol-engine/
├── Dockerfile
├── README.md
├── main.py
├── pricing.ipynb
├── models/
│   ├── black_scholes.py
│   ├── heston.py
│   └── heston_monte_carlo.py
└── products/
    ├── european_call.py
    ├── european_put.py
    └── options.py
```

## Reproducible steps

```bash
git clone https://github.com/velvetlew/stoch-vol-engine.git
```

```bash
docker run --rm -v "$(pwd)":/app stoch-vol-engine jupyter nbconvert --to html --execute pricing.ipynb
```

```bash
open -a "Google Chrome" pricing.html
```
