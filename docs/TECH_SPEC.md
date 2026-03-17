# Stock Analysis Web Application - Technical Specification

## 1. Overview

A Flask-based web application providing fundamental analysis, technical analysis, and AI-powered insights for stock market analysis.

### 1.1 Goals
- Provide comprehensive fundamental analysis (financial statements, ratios, valuation)
- Deliver technical analysis with indicators and chart patterns
- Generate AI-powered insights including sentiment analysis and predictions
- Server-rendered UI with Jinja2 templates and interactive charts

### 1.2 Non-Goals
- Real-time streaming data (batch/on-demand refresh only)
- Trading execution or brokerage integration
- Portfolio management or transaction tracking

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Jinja2)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Dashboard│  │Fundamental│  │Technical │  │  AI Insights    │ │
│  │   Page   │  │  Analysis │  │ Analysis │  │     Page        │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Application                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Route Handlers                         │   │
│  │  /api/stock/<symbol>  /api/fundamental  /api/technical   │   │
│  │  /api/ai-insights     /api/search                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Service Layer                          │   │
│  │  StockDataService  FundamentalService  TechnicalService  │   │
│  │  AIInsightsService  CacheService                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External APIs                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ yfinance │  │ Alpha    │  │ News API │  │ OpenAI/Azure     │ │
│  │          │  │ Vantage  │  │          │  │ (LLM)            │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Storage                                  │
│  ┌──────────────────┐  ┌────────────────────────────────────┐   │
│  │  SQLite (Dev)    │  │  Redis Cache (Optional)            │   │
│  │  PostgreSQL(Prod)│  │  - API response caching            │   │
│  └──────────────────┘  └────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. External APIs

### 3.1 Stock Data Provider - yfinance (Primary)
- **Purpose**: Historical prices, financial statements, company info
- **Rate Limits**: Unofficial API, ~2000 requests/hour recommended
- **Cost**: Free
- **Data Available**:
  - Historical OHLCV data
  - Income statement, balance sheet, cash flow
  - Company info, sector, industry
  - Dividends and splits

### 3.2 Alpha Vantage (Secondary/Backup)
- **Purpose**: Backup data source, additional indicators
- **Rate Limits**: 5 calls/min (free), 75 calls/min (premium)
- **Cost**: Free tier available, $49.99/month premium
- **API Key Required**: Yes
- **Endpoints Used**:
  - `TIME_SERIES_DAILY` - Daily prices
  - `OVERVIEW` - Company fundamentals
  - `INCOME_STATEMENT`, `BALANCE_SHEET`, `CASH_FLOW`

### 3.3 News API
- **Purpose**: News articles for sentiment analysis
- **Rate Limits**: 100 requests/day (free), 250,000/month (business)
- **Cost**: Free tier available
- **API Key Required**: Yes
- **Endpoints Used**:
  - `/v2/everything` - Search news by keyword/company

### 3.4 OpenAI / Azure OpenAI
- **Purpose**: AI-powered analysis, sentiment scoring, predictions
- **Rate Limits**: Varies by tier
- **Cost**: Pay-per-token
- **API Key Required**: Yes
- **Models Used**:
  - `gpt-4o` or `gpt-4o-mini` for analysis
- **Use Cases**:
  - News sentiment analysis
  - Investment thesis generation
  - Risk assessment summaries

---

## 4. Internal APIs

### 4.1 Stock Data Endpoints

#### `GET /api/stock/<symbol>`
Fetch basic stock information and current price.

**Response**:
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "current_price": 178.50,
  "market_cap": 2800000000000,
  "pe_ratio": 28.5,
  "dividend_yield": 0.005,
  "52_week_high": 199.62,
  "52_week_low": 143.90
}
```

#### `GET /api/stock/<symbol>/history`
Fetch historical price data.

**Query Parameters**:
- `period`: `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `max` (default: `1y`)
- `interval`: `1d`, `1wk`, `1mo` (default: `1d`)

**Response**:
```json
{
  "symbol": "AAPL",
  "period": "1y",
  "interval": "1d",
  "data": [
    {"date": "2024-01-02", "open": 185.5, "high": 186.2, "low": 184.1, "close": 185.8, "volume": 45000000},
    ...
  ]
}
```

### 4.2 Fundamental Analysis Endpoints

#### `GET /api/fundamental/<symbol>`
Comprehensive fundamental analysis.

**Response**:
```json
{
  "symbol": "AAPL",
  "financials": {
    "income_statement": {...},
    "balance_sheet": {...},
    "cash_flow": {...}
  },
  "ratios": {
    "profitability": {
      "gross_margin": 0.438,
      "operating_margin": 0.297,
      "net_margin": 0.253,
      "roe": 0.147,
      "roa": 0.208
    },
    "liquidity": {
      "current_ratio": 0.988,
      "quick_ratio": 0.843
    },
    "leverage": {
      "debt_to_equity": 1.81,
      "interest_coverage": 29.4
    },
    "valuation": {
      "pe_ratio": 28.5,
      "pb_ratio": 47.2,
      "ps_ratio": 7.4,
      "ev_ebitda": 22.1,
      "peg_ratio": 2.8
    },
    "efficiency": {
      "asset_turnover": 1.09,
      "inventory_turnover": 34.5
    }
  },
  "growth": {
    "revenue_growth_yoy": 0.028,
    "earnings_growth_yoy": 0.109,
    "revenue_cagr_5y": 0.082
  }
}
```

#### `GET /api/fundamental/<symbol>/statements`
Raw financial statements.

**Query Parameters**:
- `type`: `income`, `balance`, `cashflow`, `all` (default: `all`)
- `period`: `annual`, `quarterly` (default: `annual`)
- `limit`: Number of periods (default: `4`)

### 4.3 Technical Analysis Endpoints

#### `GET /api/technical/<symbol>`
Technical indicators and signals.

**Query Parameters**:
- `period`: Time period for analysis (default: `1y`)
- `indicators`: Comma-separated list (default: `sma,ema,rsi,macd,bbands`)

**Response**:
```json
{
  "symbol": "AAPL",
  "indicators": {
    "sma": {"sma_20": 176.5, "sma_50": 174.2, "sma_200": 168.9},
    "ema": {"ema_12": 177.1, "ema_26": 175.8},
    "rsi": {"rsi_14": 58.3, "signal": "neutral"},
    "macd": {"macd": 1.42, "signal": 1.15, "histogram": 0.27, "trend": "bullish"},
    "bbands": {"upper": 182.5, "middle": 176.5, "lower": 170.5, "width": 0.068}
  },
  "signals": {
    "trend": "bullish",
    "momentum": "neutral",
    "volatility": "low",
    "support_levels": [170.0, 165.0, 160.0],
    "resistance_levels": [180.0, 185.0, 190.0]
  },
  "summary": {
    "overall_signal": "buy",
    "confidence": 0.65,
    "reasons": [
      "Price above 200-day SMA",
      "MACD bullish crossover",
      "RSI in neutral zone with room to rise"
    ]
  }
}
```

#### `GET /api/technical/<symbol>/chart-data`
Data formatted for charting libraries.

**Query Parameters**:
- `period`: `1mo`, `3mo`, `6mo`, `1y` (default: `6mo`)
- `overlays`: `sma,ema,bbands` (default: `sma`)

### 4.4 AI Insights Endpoints

#### `GET /api/ai/<symbol>/sentiment`
News sentiment analysis.

**Query Parameters**:
- `days`: Number of days to analyze (default: `7`)

**Response**:
```json
{
  "symbol": "AAPL",
  "sentiment": {
    "overall_score": 0.65,
    "label": "positive",
    "confidence": 0.82
  },
  "news_analyzed": 15,
  "key_topics": ["iPhone sales", "AI features", "Services growth"],
  "articles": [
    {
      "title": "Apple Reports Strong Q4 Earnings",
      "source": "Reuters",
      "date": "2024-01-15",
      "sentiment": 0.8,
      "url": "https://..."
    }
  ]
}
```

#### `GET /api/ai/<symbol>/analysis`
AI-generated investment analysis.

**Response**:
```json
{
  "symbol": "AAPL",
  "analysis": {
    "summary": "Apple shows strong fundamentals with consistent revenue growth...",
    "strengths": ["Strong brand loyalty", "Services segment growth", "Cash reserves"],
    "weaknesses": ["iPhone dependency", "China exposure", "Regulatory risks"],
    "opportunities": ["AI integration", "AR/VR market", "Healthcare"],
    "threats": ["Competition", "Supply chain", "Economic downturn"]
  },
  "recommendation": {
    "action": "hold",
    "confidence": 0.72,
    "target_price": {"low": 165, "mid": 185, "high": 210},
    "time_horizon": "12 months"
  },
  "risk_assessment": {
    "overall_risk": "medium",
    "volatility_risk": "low",
    "fundamental_risk": "low",
    "market_risk": "medium"
  }
}
```

#### `POST /api/ai/compare`
Compare multiple stocks.

**Request Body**:
```json
{
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "criteria": ["valuation", "growth", "profitability"]
}
```

### 4.5 Search Endpoint

#### `GET /api/search`
Search for stocks by name or symbol.

**Query Parameters**:
- `q`: Search query (required)
- `limit`: Max results (default: `10`)

**Response**:
```json
{
  "results": [
    {"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"},
    {"symbol": "APLE", "name": "Apple Hospitality REIT", "exchange": "NYSE"}
  ]
}
```

---

## 5. Data Models

### 5.1 Database Schema

```sql
-- Stock metadata cache
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    exchange VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical price data cache
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(12, 4),
    high DECIMAL(12, 4),
    low DECIMAL(12, 4),
    close DECIMAL(12, 4),
    adj_close DECIMAL(12, 4),
    volume BIGINT,
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE(stock_id, date)
);

-- Financial statements cache
CREATE TABLE financial_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    statement_type VARCHAR(20) NOT NULL,  -- income, balance, cashflow
    period_type VARCHAR(10) NOT NULL,      -- annual, quarterly
    period_end DATE NOT NULL,
    data JSON NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE(stock_id, statement_type, period_type, period_end)
);

-- Calculated ratios cache
CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    period_end DATE NOT NULL,
    ratios JSON NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE(stock_id, period_end)
);

-- AI analysis cache
CREATE TABLE ai_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,  -- sentiment, full_analysis, comparison
    data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

-- User watchlists (future feature)
CREATE TABLE watchlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE watchlist_stocks (
    watchlist_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (watchlist_id, stock_id),
    FOREIGN KEY (watchlist_id) REFERENCES watchlists(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
);
```

### 5.2 Pydantic Models

```python
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class StatementType(str, Enum):
    INCOME = "income"
    BALANCE = "balance"
    CASHFLOW = "cashflow"

class PeriodType(str, Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"

class SignalType(str, Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

class SentimentLabel(str, Enum):
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

# Stock Models
class StockInfo(BaseModel):
    symbol: str
    name: str
    sector: Optional[str]
    industry: Optional[str]
    exchange: Optional[str]
    current_price: Optional[float]
    market_cap: Optional[int]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    week_52_high: Optional[float]
    week_52_low: Optional[float]

class PriceBar(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class PriceHistory(BaseModel):
    symbol: str
    period: str
    interval: str
    data: List[PriceBar]

# Fundamental Models
class ProfitabilityRatios(BaseModel):
    gross_margin: Optional[float]
    operating_margin: Optional[float]
    net_margin: Optional[float]
    roe: Optional[float]
    roa: Optional[float]

class LiquidityRatios(BaseModel):
    current_ratio: Optional[float]
    quick_ratio: Optional[float]

class LeverageRatios(BaseModel):
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]

class ValuationRatios(BaseModel):
    pe_ratio: Optional[float]
    pb_ratio: Optional[float]
    ps_ratio: Optional[float]
    ev_ebitda: Optional[float]
    peg_ratio: Optional[float]

class FinancialRatios(BaseModel):
    profitability: ProfitabilityRatios
    liquidity: LiquidityRatios
    leverage: LeverageRatios
    valuation: ValuationRatios

class GrowthMetrics(BaseModel):
    revenue_growth_yoy: Optional[float]
    earnings_growth_yoy: Optional[float]
    revenue_cagr_5y: Optional[float]

class FundamentalAnalysis(BaseModel):
    symbol: str
    financials: Dict[str, Any]
    ratios: FinancialRatios
    growth: GrowthMetrics

# Technical Models
class TechnicalIndicators(BaseModel):
    sma: Dict[str, float]
    ema: Dict[str, float]
    rsi: Dict[str, Any]
    macd: Dict[str, Any]
    bbands: Dict[str, float]

class TechnicalSignals(BaseModel):
    trend: str
    momentum: str
    volatility: str
    support_levels: List[float]
    resistance_levels: List[float]

class TechnicalSummary(BaseModel):
    overall_signal: SignalType
    confidence: float
    reasons: List[str]

class TechnicalAnalysis(BaseModel):
    symbol: str
    indicators: TechnicalIndicators
    signals: TechnicalSignals
    summary: TechnicalSummary

# AI Models
class NewsArticle(BaseModel):
    title: str
    source: str
    date: date
    sentiment: float
    url: str

class SentimentResult(BaseModel):
    overall_score: float
    label: SentimentLabel
    confidence: float

class SentimentAnalysis(BaseModel):
    symbol: str
    sentiment: SentimentResult
    news_analyzed: int
    key_topics: List[str]
    articles: List[NewsArticle]

class SWOTAnalysis(BaseModel):
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class PriceTarget(BaseModel):
    low: float
    mid: float
    high: float

class Recommendation(BaseModel):
    action: SignalType
    confidence: float
    target_price: PriceTarget
    time_horizon: str

class RiskAssessment(BaseModel):
    overall_risk: str
    volatility_risk: str
    fundamental_risk: str
    market_risk: str

class AIAnalysis(BaseModel):
    symbol: str
    analysis: SWOTAnalysis
    recommendation: Recommendation
    risk_assessment: RiskAssessment
```

---

## 6. Constraints & Limitations

### 6.1 Rate Limits
| API | Free Tier Limit | Mitigation Strategy |
|-----|-----------------|---------------------|
| yfinance | ~2000 req/hr | Cache aggressively, batch requests |
| Alpha Vantage | 5 req/min | Use as fallback only |
| News API | 100 req/day | Cache for 1 hour, limit news fetches |
| OpenAI | Varies | Cache AI responses for 24 hours |

### 6.2 Data Freshness
| Data Type | Cache Duration | Refresh Strategy |
|-----------|---------------|------------------|
| Stock info | 1 hour | On-demand refresh |
| Price history | 1 day | Daily batch update |
| Financial statements | 1 week | Weekly batch update |
| Technical indicators | 1 hour | On-demand calculation |
| News sentiment | 1 hour | On-demand refresh |
| AI analysis | 24 hours | On-demand regeneration |

### 6.3 Technical Constraints
- **No real-time data**: All data is delayed (15-20 min for free APIs)
- **US stocks only**: Initial version supports NYSE/NASDAQ only
- **Historical data limits**: yfinance provides ~20 years of daily data
- **AI token limits**: Analysis prompts capped at 4000 tokens input

### 6.4 Security Constraints
- API keys stored in environment variables, never in code
- Rate limiting on all endpoints (100 req/min per IP)
- Input validation on all user inputs (symbol format, date ranges)
- No user authentication in v1 (stateless)

---

## 7. Project Structure

```
stock_analysis/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_data.py        # Stock data fetching
│   │   ├── fundamental.py       # Fundamental analysis
│   │   ├── technical.py         # Technical analysis
│   │   ├── ai_insights.py       # AI-powered analysis
│   │   └── cache.py             # Caching layer
│   ├── api/
│   │   ├── __init__.py
│   │   ├── stock.py             # Stock endpoints
│   │   ├── fundamental.py       # Fundamental endpoints
│   │   ├── technical.py         # Technical endpoints
│   │   └── ai.py                # AI endpoints
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── stock.html
│   │   ├── fundamental.html
│   │   ├── technical.html
│   │   └── ai_insights.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── charts.js
│           └── main.js
├── tests/
│   ├── __init__.py
│   ├── test_services/
│   ├── test_api/
│   └── conftest.py
├── migrations/                   # Alembic migrations
├── docs/
│   └── TECH_SPEC.md
├── .env.example
├── requirements.txt
├── README.md
└── run.py                       # Entry point
```

---

## 8. Dependencies

```
# Core
flask>=3.0.0
flask-sqlalchemy>=3.1.0
flask-migrate>=4.0.0
pydantic>=2.5.0

# Data & Analysis
yfinance>=0.2.36
pandas>=2.1.0
numpy>=1.26.0
ta>=0.11.0                       # Technical analysis library

# AI & NLP
openai>=1.10.0
tiktoken>=0.5.0

# HTTP & Caching
requests>=2.31.0
redis>=5.0.0                     # Optional, for production caching

# Utilities
python-dotenv>=1.0.0

# Development
pytest>=7.4.0
pytest-cov>=4.1.0
```

---

## 9. Environment Variables

```bash
# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///stock_analysis.db

# External APIs
ALPHA_VANTAGE_API_KEY=your-key
NEWS_API_KEY=your-key

# OpenAI / Azure OpenAI
OPENAI_API_KEY=your-key
# OR for Azure:
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Optional
REDIS_URL=redis://localhost:6379/0
```

---

## 10. Future Enhancements (Out of Scope for v1)

1. **User Authentication**: Login, saved watchlists, personalized alerts
2. **Real-time Data**: WebSocket integration for live prices
3. **International Markets**: Support for non-US exchanges
4. **Options Analysis**: Greeks, options chain, strategy builder
5. **Backtesting**: Historical strategy testing
6. **Mobile App**: React Native companion app
7. **Notifications**: Email/push alerts for price targets
