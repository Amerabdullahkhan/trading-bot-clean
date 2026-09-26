# Trading Bot Clean

A simple Python trading signal analyzer for paper trading.

This project is for learning and research only. It does not claim any risk-free strategy or guaranteed profit. It is designed to show how a small trading system can:

- scan multiple symbols
- compute trend and momentum indicators
- combine signals into a buy/sell/hold decision
- apply basic risk limits
- simulate trades with a paper broker

## Requirements

- Python 3.11+
- Git
- PowerShell or Command Prompt

## Quick start

```powershell
cd Desktop\trading-bot-clean
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Run the dashboard

```powershell
python -m app.dashboard
```

## Risk note

Trading carries real risk. This project is intentionally designed as a paper-trading framework with risk checks, but it is not a guaranteed-profit or risk-free system.
