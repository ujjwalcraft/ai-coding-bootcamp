# AI Coding Bootcamp - Facilitator Guide

## Overview

This guide walks you through a **~55-60 minute bootcamp** demonstrating five AI-assisted coding capabilities using a Stock Price Analyzer CLI as the demo project.

**Project Location:** `stock_analysis/src/stock_cli.py`

---

## Attendee Pre-Requisites (Share Before Session)

**Send this to attendees 1 day before:**

> ### Setup Instructions (2 min)
> 
> 1. **Have Python 3.9+ installed** — check with `python --version`
> 2. **Have an AI coding assistant** — Windsurf, Cursor, Copilot, or similar
> 3. **Download the project** — [link to repo/zip]
> 4. **Run setup:**
>    ```bash
>    cd stock_analysis
>    python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
>    ```
> 5. **Verify:** `python src/stock_cli.py price AAPL` should show Apple's stock price
>
> That's it! No API keys needed for most exercises.

---

## Facilitator Pre-Session Setup (5 min before)

1. **Verify the CLI runs:**
   ```bash
   python src/stock_cli.py price AAPL
   ```

2. **Have these files open in your IDE:**
   - `src/stock_cli.py` (main demo file)
   - This guide (for reference)

3. **Optional:** If demoing AI analysis feature, set `OPENAI_API_KEY` env var

---

## Section 1: Feature Generation (~15 min)

### Learning Objective
Show how to describe requirements clearly and iterate on generated code.

### Demo Script

**1. Show the incomplete `analyze_stock()` function (line ~85):**

```python
def analyze_stock(ticker):
    """
    AI-powered stock analysis.
    
    TODO: Implement this using OpenAI/Azure to:
    1. Summarize recent news sentiment
    2. Generate investment thesis
    3. Identify key risks
    """
    print(f"AI analysis for {ticker} is not yet implemented.")
```

**2. Ask the AI to implement it:**

> "Implement the `analyze_stock` function. It should:
> - Fetch recent news about the stock using yfinance
> - Send the news to OpenAI/Azure to analyze sentiment
> - Return a summary with bull case, bear case, and key risks
> - Handle errors gracefully if API keys aren't set"

**3. Talking Points:**
- **Be specific** about inputs/outputs
- **Mention error handling** upfront
- **Iterate** — first pass may need refinement
- Show how to ask for "add retry logic" or "make the prompt better"

**4. Optional Extension:**
Ask AI to add a new command: `python stock_cli.py top-movers --count 5`

---

## Section 2: Debugging (~10 min)

### Learning Objective
Demonstrate how to provide context (error + code) and let AI diagnose root cause.

### Demo Script

**1. Trigger Bug #1 — Off-by-one error:**

```bash
python src/stock_cli.py history AAPL --days 7
```

Point out that `get_date_range()` has `days - 1` which is wrong.

**2. Ask AI to debug:**

> "The history command is returning one fewer day than expected. Here's the function:
> ```python
> def get_date_range(days: int):
>     end_date = datetime.now()
>     start_date = end_date - timedelta(days=days - 1)
>     return start_date, end_date
> ```
> What's wrong?"

**3. Trigger Bug #2 — Invalid ticker:**

```bash
python src/stock_cli.py price INVALIDTICKER123
```

This will crash with `KeyError`. Ask AI:

> "This crashes when I use an invalid ticker. How do I add proper error handling?"

**4. Talking Points:**
- **Provide the error message** — stack traces help
- **Show relevant code** — don't make AI guess
- **Ask for root cause**, not just a fix
- Discuss: "Fix the symptom vs. fix the root cause"

---

## Section 3: Refactoring (~10 min)

### Learning Objective
Show how to request specific refactors vs. open-ended "make it better."

### Demo Script

**1. Point out the `display_comparison()` function (line ~55):**

This function has duplicated code for printing stock info.

**2. Ask for specific refactors:**

> "Refactor `display_comparison()` to:
> 1. Extract a helper function `format_stock_info(ticker, info)` that returns formatted string
> 2. Add type hints
> 3. Use f-string formatting consistently"

**3. Ask for structural refactor:**

> "The main() function uses if/elif for commands. Refactor to use a command pattern with a dictionary mapping command names to handler functions."

**4. Talking Points:**
- **Be specific** — "extract X into Y" is better than "clean this up"
- **One refactor at a time** — easier to review
- **Ask AI to explain** the refactoring rationale
- Discuss: When to refactor vs. when to leave it alone

---

## Section 4: Test Generation (~10 min)

### Learning Objective
Show how to specify test framework, coverage targets, and edge cases.

### Demo Script

**1. Ask for unit tests:**

> "Generate pytest tests for the `get_date_range()` function. Include:
> - Happy path with various day counts (1, 7, 30)
> - Edge case: days=0
> - Edge case: negative days
> - Verify the date math is correct"

**2. Ask for tests with mocking:**

> "Generate pytest tests for `fetch_stock_price()` that:
> - Mock the yfinance API
> - Test successful response
> - Test invalid ticker (empty info dict)
> - Test network error"

**3. Show the generated test file structure:**

```python
# tests/test_stock_cli.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from src.stock_cli import get_date_range, fetch_stock_price

class TestGetDateRange:
    def test_seven_days(self):
        ...
    
    def test_edge_case_zero_days(self):
        ...

class TestFetchStockPrice:
    @patch('src.stock_cli.yf.Ticker')
    def test_valid_ticker(self, mock_ticker):
        ...
```

**4. Talking Points:**
- **Specify the framework** (pytest, unittest, etc.)
- **Ask for specific scenarios** — happy path, edge cases, errors
- **Request mocking** for external dependencies
- Discuss: Test coverage vs. test quality

---

## Section 5: Prompt Optimization (~10 min)

### Learning Objective
Show how better prompts get better AI outputs — both for coding queries AND for LLM features in the app.

### Demo Script

**Option A: Optimize the AI analysis prompt (if you implemented it in Section 1)**

**1. Show a basic prompt:**

```python
prompt = f"Analyze this stock: {ticker}. Here's recent news: {news}"
```

**2. Ask AI to improve it:**

> "Improve this prompt for stock analysis. Make it:
> - More structured with clear sections
> - Include few-shot examples of good analysis
> - Specify output format (JSON with bull_case, bear_case, risks)
> - Add constraints (be objective, cite sources)"

**3. Compare outputs** from basic vs. optimized prompts.

---

**Option B: Optimize your own AI coding queries**

**1. Show a vague query:**

> "Fix the bug"

**2. Show an optimized query:**

> "The `fetch_stock_price()` function crashes with KeyError when given an invalid ticker like 'INVALIDXYZ'. The yfinance library returns an empty dict for `stock.info` in this case. Add error handling that:
> 1. Checks if required keys exist
> 2. Returns a user-friendly error message
> 3. Doesn't crash the CLI"

**3. Talking Points:**
- **Context matters** — what, where, why
- **Specify constraints** — format, length, style
- **Few-shot examples** dramatically improve output
- **Iterate** — first response is rarely perfect

---

## Wrap-Up (~5 min)

### Key Takeaways

1. **Feature Generation:** Be specific about requirements, iterate on output
2. **Debugging:** Provide error + code context, ask for root cause
3. **Refactoring:** Request specific changes, one at a time
4. **Test Generation:** Specify framework, scenarios, and mocking needs
5. **Prompt Optimization:** Structure, examples, and constraints improve output

### Q&A Prompts

- "What's the most surprising thing AI got right/wrong?"
- "When would you NOT use AI for coding?"
- "How do you verify AI-generated code is correct?"

---

## Appendix: Intentional Bugs in the Demo Code

| Bug | Location | Issue | Fix |
|-----|----------|-------|-----|
| #1 | `get_date_range()` | Off-by-one: `days - 1` | Change to `days` |
| #2 | `fetch_stock_price()` | No error handling for invalid ticker | Add try/except and key checks |
| #3 | `fetch_stock_price()` | KeyError on missing keys | Use `.get()` with defaults |
| #4 | `fetch_history()` | `period` param is wrong | Use `start`/`end` dates instead |

## Appendix: Refactoring Opportunities

| Area | Current State | Suggested Refactor |
|------|--------------|-------------------|
| `display_comparison()` | Duplicated print statements | Extract `format_stock_info()` helper |
| `main()` | if/elif command dispatch | Command pattern with dict |
| Type hints | Missing | Add throughout |
| Error handling | Inconsistent | Centralized error handler |

---

## Appendix: Sample Test File

Save as `tests/test_stock_cli.py`:

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from stock_cli import get_date_range, fetch_stock_price


class TestGetDateRange:
    """Tests for the get_date_range function."""
    
    def test_seven_days_returns_correct_range(self):
        """Verify 7 days returns a 7-day range."""
        start, end = get_date_range(7)
        delta = end - start
        # BUG: Currently returns 6 days due to off-by-one error
        # After fix, this should pass
        assert delta.days == 7 or delta.days == 6  # Flexible for demo
    
    def test_one_day_returns_same_day(self):
        """Edge case: 1 day should return ~0 day delta."""
        start, end = get_date_range(1)
        delta = end - start
        assert delta.days <= 1
    
    def test_thirty_days(self):
        """Standard case: 30 days."""
        start, end = get_date_range(30)
        delta = end - start
        assert 29 <= delta.days <= 30


class TestFetchStockPrice:
    """Tests for fetch_stock_price with mocked yfinance."""
    
    @patch('stock_cli.yf.Ticker')
    def test_valid_ticker_returns_price_info(self, mock_ticker_class):
        """Happy path: valid ticker returns expected fields."""
        mock_ticker = MagicMock()
        mock_ticker.info = {
            'currentPrice': 150.0,
            'shortName': 'Apple Inc.',
            'regularMarketChangePercent': 1.5,
        }
        mock_ticker_class.return_value = mock_ticker
        
        result = fetch_stock_price('AAPL')
        
        assert result['symbol'] == 'AAPL'
        assert result['price'] == 150.0
        assert result['name'] == 'Apple Inc.'
    
    @patch('stock_cli.yf.Ticker')
    def test_invalid_ticker_raises_key_error(self, mock_ticker_class):
        """Invalid ticker should raise KeyError (current buggy behavior)."""
        mock_ticker = MagicMock()
        mock_ticker.info = {}  # Empty dict for invalid ticker
        mock_ticker_class.return_value = mock_ticker
        
        with pytest.raises(KeyError):
            fetch_stock_price('INVALIDXYZ')
```

Run with: `pytest tests/ -v`
