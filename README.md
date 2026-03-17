# Stock Price Analyzer CLI - Bootcamp Demo

A starter project for demonstrating AI coding assistant capabilities.

## Quick Setup (2 minutes)

### Prerequisites
- Python 3.9+ installed
- Any AI coding assistant (Windsurf, Cursor, Copilot, etc.)

### One-Command Setup

```bash
# Clone/navigate to the project, then:
cd stock_analysis
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

**Windows:**
```cmd
cd stock_analysis
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
```

### Verify It Works

```bash
python src/stock_cli.py --help
python src/stock_cli.py price AAPL
```

You should see Apple's current stock price. If you see an error, check your internet connection.

---

## What We'll Build

This CLI fetches stock data and has **intentional bugs and gaps** for learning:

| Command | What it does |
|---------|--------------|
| `price AAPL` | Get current price |
| `history AAPL --days 30` | Get price history |
| `compare AAPL MSFT` | Compare two stocks |
| `analyze AAPL` | AI analysis (not implemented yet!) |

---

## Bootcamp Sections

1. **Feature Generation** — Implement the `analyze` command
2. **Debugging** — Fix the bugs in the code
3. **Refactoring** — Improve code structure
4. **Test Generation** — Add pytest tests
5. **Prompt Optimization** — Write better AI prompts

See `docs/BOOTCAMP_FACILITATOR_GUIDE.md` for the full facilitator script.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: yfinance` | Run `pip install -r requirements.txt` |
| `No module named 'src'` | Run from the `stock_analysis` folder |
| Network error | Check internet connection, yfinance needs web access |
| `KeyError` on price command | This is an intentional bug! We'll fix it in the debugging section. |

---

## Optional: AI Analysis Feature

If you want to demo the AI analysis feature (Section 1), you'll need an OpenAI API key:

```bash
export OPENAI_API_KEY="your-key-here"
```

This is **optional** — the other 4 sections work without any API keys.
