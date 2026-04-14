# Stablecoin FX & Execution Monitoring System

## Overview

This project is a real-time stablecoin FX and liquidity monitoring system designed to analyze pricing consistency across fragmented crypto markets and simulate execution decision-making logic.

It aggregates market data from multiple centralized exchanges, evaluates cross-venue pricing relationships, and generates execution signals based on deviations from a stablecoin USD anchor assumption.

The system reflects core concepts used in crypto market making and execution trading environments, including liquidity fragmentation, peg stability monitoring, and execution logic design.

---

## Market Context

Crypto markets are highly fragmented across exchanges, leading to temporary pricing inefficiencies due to:

- Liquidity differences
- Order book fragmentation
- Latency between venues
- Stablecoin peg dynamics

This system models how execution desks monitor these inefficiencies and identify potential trading opportunities.

---

## Key Assumptions

The system is built on the following market structure assumptions:

- USDC/USD is treated as a hard peg reference (≈ 1.0)
- USDT/USD is derived from major liquidity venues (Kraken / Bitfinex)
- Cross-stablecoin relationships can be inferred via FX reconstruction

These assumptions allow the system to evaluate pricing consistency across stablecoin pairs.

---

## System Architecture

The system follows a modular execution pipeline:

Market Data Layer → Normalization Layer → Signal Generation → Execution Logic → Output Interface

---

## Core Components

### 1. Market Data Layer
- Fetches real-time price data from multiple exchanges
- Sources include Kraken, Binance, and Bitfinex APIs

### 2. Pricing Normalization
- Constructs implied FX relationships between stablecoins
- Aligns pricing into a consistent USD-referenced framework

### 3. Signal Generation
- Detects deviations from expected peg relationships
- Identifies cross-venue pricing inefficiencies

### 4. Execution Logic
- Converts signals into actionable execution decisions
- Simulates trading responses under different market conditions

### 5. Monitoring Interface
- Outputs results via Telegram bot for real-time visibility

---

## Execution Logic

The system identifies potential trading opportunities when observed pricing deviates from expected stablecoin FX relationships beyond a defined threshold.

Decision logic:

- If deviation > threshold → execution signal triggered
- If within threshold → no action
- Signals represent potential arbitrage or mispricing conditions

---

## Example Use Case

1. System collects real-time prices from multiple exchanges  
2. Computes implied FX relationships between stablecoins  
3. Compares observed vs expected peg relationships  
4. Generates execution signal if inconsistency is detected  
5. Outputs result via Telegram interface

---

## Tech Stack

- Python
- REST APIs (Kraken, Binance, Bitfinex)
- Telegram Bot API
- Basic financial modeling logic

---

## Trading Relevance

This project demonstrates understanding of:

- Stablecoin FX structure and peg mechanisms
- Cross-venue liquidity fragmentation
- Execution decision frameworks
- Real-time market monitoring systems
- Basic market making logic design

It simulates how execution traders and liquidity providers monitor pricing inefficiencies and respond to market dislocations in fragmented digital asset markets.

---

## Disclaimer

This system is a simulation tool designed to model stablecoin FX pricing relationships and execution decision logic in fragmented crypto markets.

It does not execute real trades, connect to live trading venues, or interact with brokerage or exchange execution systems.
