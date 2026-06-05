# Stoch-Vol-Engine

## Project Description

This project implements stochastic volatility option pricing using the Heston model. It compares option prices from:

- Black-Scholes model
- Analytic Heston model
- Heston Monte Carlo simulation

The project also includes a Jupyter notebook workflow for generating an HTML report.

## Project Structure

```text
stoch-vol-engine/
|-- Dockerfile
|-- README.md
|-- main.py
|-- pricing.ipynb
|-- bs_vs_heston.png
|-- requirements.txt
|-- models/
|   |-- black_scholes.py
|   |-- heston.py
|   `-- heston_monte_carlo.py
`-- products/
    |-- european_call.py
    |-- european_put.py
    `-- options.py
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/velvetlew/stoch-vol-engine.git
```

```bash
cd stoch-vol-engine
```

Run the published Docker image:

```bash
docker run --rm -v "$(pwd)":/app velvetlew/stoch-vol-engine:plat jupyter nbconvert --to html --execute pricing.ipynb
```

This generates:

```text
pricing.html
```

Open the generated HTML report:

```bash
open pricing.html
```

On macOS, you can also open it in Google Chrome:

```bash
open -a "Google Chrome" pricing.html
```

## macOS / Apple Silicon Notes

The prebuilt Docker image may not run directly on Apple Silicon Macs if it is not published for `linux/arm64`.

If this command:

```bash
docker run --rm -v "$(pwd)":/app velvetlew/stoch-vol-engine jupyter nbconvert --to html --execute pricing.ipynb
```

fails with an error similar to:

```text
no matching manifest for linux/arm64/v8 in the manifest list entries
```

build the Docker image locally instead:

```bash
docker build -t stoch-vol-engine-local .
docker run --rm -v "$(pwd)":/app stoch-vol-engine-local jupyter nbconvert --to html --execute pricing.ipynb --ExecutePreprocessor.startup_timeout=120 --ExecutePreprocessor.timeout=600
```

Forcing the prebuilt image with `--platform linux/amd64` may also be slow or unstable on Apple Silicon because it runs under emulation.

To make the original Docker command work across Windows, Linux, Intel Mac and Apple Silicon Mac, publish a multi-platform Docker image:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t velvetlew/stoch-vol-engine:latest \
  --push .
```

After that, this command should work on more machines:

```bash
docker run --rm -v "$(pwd)":/app velvetlew/stoch-vol-engine jupyter nbconvert --to html --execute pricing.ipynb
```
