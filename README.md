# Cross-Market Stablecoin Execution Monitor

## Overview

This project is a lightweight execution-focused monitoring system designed to analyze cross-market pricing consistency in stablecoin FX markets.

It compares:

- Direct USDT/USD pricing from centralized exchanges (Kraken, Bitfinex)
- Implied USDT/USD pricing derived from Binance USDC/USDT market

under the assumption that USDC ≈ USD.

The goal is to detect pricing inconsistencies across fragmented venues and evaluate whether a theoretical execution opportunity exists after considering basic execution constraints.

---

## Core Concept

The system models two pricing paths:

### 1. Direct Market Price (CEX)
USDT/USD observed directly from centralized exchanges:
- Kraken
- Bitfinex

### 2. Synthetic Market Price (Binance-derived)
USDT/USD implied via:

USDT → USDC → USD

Given:
- USDC/USDT is traded on Binance
- USDC is assumed to be pegged to USD

Implied pricing:

USDT/USD ≈ 1 / (USDC/USDT)

---

## Execution Logic

The system follows a simplified execution-aware workflow:

### Step 1: Venue Selection
- Select the best available USDT/USD execution venue (Kraken vs Bitfinex)
- Compare effective prices under fee assumptions

### Step 2: Price Normalization
- Convert Binance USDC/USDT into implied USDT/USD

### Step 3: Cross-Market Spread
Spread is defined as:

CEX USDT/USD − Binance implied USDT/USD

### Step 4: Decision Layer
A trade signal is generated only when:

|Spread| > threshold

Where threshold represents minimum executable edge after considering:
- Fees
- Operational buffer
- Execution uncertainty

---

## Key Assumptions

### Market Assumptions
- USDC is fully pegged to USD (USDC ≈ 1 USD)
- Markets are liquid enough to execute at quoted prices

### Execution Assumptions
- All executions are assumed to be **maker orders**
- No slippage or order book depth modeling is included
- Latency is ignored (instantaneous execution assumption)

### Fee Structure
- Kraken: maker fee = 0, taker fee = 1 bp (not used in this model)
- Binance: maker/taker fee = 0
- Bitfinex: withdrawal cost approximated at 2 bps

---

## Signal Interpretation

The system outputs:

- **Spread**
- **Threshold-adjusted signal**

### Signal Logic:

- Spread > threshold  
  → Sell CEX USDT / Buy Binance-implied USDT

- Spread < -threshold  
  → Buy CEX USDT / Sell Binance-implied USDT

- Otherwise  
  → No trade (no sufficient edge)

---

## Example Output
📊 Cross-Market Consistency Monitor

USDT/USD (Kraken): 1.00020

USDT/USD (Bitfinex): 1.00018

Selected Venue: Kraken

CEX USDT/USD: 1.00020

Binance USDC/USDT: 0.99960

Implied USDT/USD: 1.00040

Spread: 0.00020

Threshold: 0.00010

Signal: TRADE，Spread - Threshold = 0.00010



---

## How to Run

1. Install dependencies
   
    pip install requests python-telegram-bot

2. Configure Telegram Bot Token
   
    TELEGRAM_BOT_TOKEN = "xxx"

3. Run script
   
    python main.py

4. Telegram usage
   
    /start → initialize bot

    /price → fetch live pricing & signal

## System Architecture
Data Layer
   
Market Data (Kraken / Bitfinex / Binance)
   
Normalization Layer
   
Implied FX Construction
   
Cross-Market Spread Calculation
   
Execution Decision Engine
   
Telegram Output Interface

## Limitations

This is a simplified execution model and does not include:

Order book depth / liquidity modeling

Slippage and partial fill risk

Latency and race conditions

Real trading fees (full structure)

Inventory or capital constraints

It should be interpreted as an execution logic prototype, not a production trading system.

## Future Improvements

Potential extensions include:

### Execution Enhancements
Bid/ask level modeling instead of last price

Slippage-aware execution simulation

Maker/taker hybrid routing logic

### Risk & PnL Layer
Position tracking

Real-time PnL attribution

Inventory-based decision making

### Market Expansion
Multi-venue arbitrage routing

Cross-asset FX modeling (BTC, ETH stable pairs)

## Summary

This project demonstrates a simplified but structured approach to:

Cross-market price consistency analysis
Synthetic FX construction
Execution-aware decision making

It reflects foundational concepts used in digital asset market making and execution trading environments.
