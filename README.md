# Cross-Venue Liquidity Conversion Monitor

A lightweight execution monitoring tool that compares **cross-venue stablecoin conversion efficiency** across centralized exchanges and synthetic FX pricing routes.

The system evaluates whether it is more efficient to convert **USDT into USD-equivalent liquidity via direct CEX venues or indirectly via Binance USDC routing**, under a simplified USDC = USD assumption.

---

## System Overview

This project models a real-world **treasury execution decision problem**:

Funds denominated in USDT may be converted into USD liquidity through two alternative routes:

### Route A — Direct CEX Conversion
- USDT → USD via:
  - Kraken
  - Bitfinex (fallback)

### Route B — Indirect Binance Conversion
- USDT → USDC (Binance)
- USDC ≈ USD (assumption: 1:1 peg)

---

## Core Logic

### 1. CEX Price Selection
The system selects the best available USDT/USD quote:

- Kraken price is used as default benchmark
- Bitfinex is used if more favorable and available

---

### 2. Synthetic USD via Binance

USDC/USDT market price is used to derive implied USD value:

USDT/USD (implied) = 1 / (USDC/USDT)

Assumption: USDC = USD (1:1 peg assumption)

---

### 3. Cross-Market Comparison

The system computes: difference = Binance implied USD - CEX USD price

---

### 4. Execution Decision Rule

If |difference| < threshold → NO TRADE

If difference > 0 → use Binance route

If difference < 0 → use CEX route

---

## Example Output

📊 Cross-Venue Liquidity Conversion Monitor

USDT/USD (Kraken): 1.0002

USDT/USD (Bitfinex): N/A

Selected CEX: KRAKEN

CEX USD value: 1.0002


Binance USDC/USDT: 0.9996

Binance effective USD: 1.0004


Difference: 0.00020


Decision: USE BINANCE ROUTE (better USD received)


---

## Project Structure

- main.py # Telegram bot execution logic

- README.md # Project documentation

---

## Features

- Real-time cross-exchange price monitoring
- Dual CEX selection (Kraken / Bitfinex fallback)
- Synthetic FX pricing via Binance USDC/USDT
- Simple execution decision engine
- Telegram bot interface for live monitoring

---

## Tech Stack

- Python 3.10+
- requests
- python-telegram-bot
- Binance / Kraken / Bitfinex public APIs

---

## Security Notice

The Telegram bot token is intentionally masked as `"xxx"` in the source code to prevent accidental exposure of credentials.

For production use, it is recommended to store credentials using environment variables:

export TELEGRAM\_BOT\_TOKEN="your-token-here"

---

## Assumptions
- USDC is assumed to be fully pegged to USD (1:1)

- No slippage or latency is modeled

- Execution fees are ignored in this simplified version

- Market data is assumed to be instantly executable

## Use Case

This tool is designed for:

- Treasury liquidity routing analysis

- Cross-venue pricing consistency checks

- Stablecoin conversion decision support

- Educational demonstration of FX-style crypto flows
