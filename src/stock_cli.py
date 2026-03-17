#!/usr/bin/env python3
"""
Stock Price Analyzer CLI - Bootcamp Demo Project

This is a STARTER project with intentional gaps for demonstrating:
1. Feature Generation - Add missing commands
2. Debugging - Fix intentional bugs
3. Refactoring - Improve code structure
4. Test Generation - Add pytest tests
5. Prompt Optimization - Improve AI analysis prompts

Usage:
    python stock_cli.py price AAPL
    python stock_cli.py history AAPL --days 30
    python stock_cli.py compare AAPL MSFT
"""

import argparse
import sys
from datetime import datetime, timedelta


# BUG #1: This function has an off-by-one error in date calculation
def get_date_range(days: int):
    """Get start and end dates for historical data."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)  # BUG: Should be just `days`
    return start_date, end_date


# BUG #2: No error handling for invalid tickers
def fetch_stock_price(ticker):
    """Fetch current stock price. Returns dict with price info."""
    import yfinance as yf
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # BUG #3: KeyError if ticker is invalid (info will be mostly empty)
    return {
        "symbol": ticker,
        "price": info["currentPrice"],
        "name": info["shortName"],
        "change": info["regularMarketChangePercent"],
    }


def fetch_history(ticker, days):
    """Fetch historical price data."""
    import yfinance as yf
    
    start, end = get_date_range(days)
    stock = yf.Ticker(ticker)
    
    # BUG #4: period parameter is wrong - should use start/end dates
    hist = stock.history(period=f"{days}d")
    
    return hist


# REFACTORING OPPORTUNITY: This function is too long and does too many things
def display_comparison(ticker1, ticker2):
    """Compare two stocks side by side."""
    import yfinance as yf
    
    stock1 = yf.Ticker(ticker1)
    stock2 = yf.Ticker(ticker2)
    
    info1 = stock1.info
    info2 = stock2.info
    
    # Duplicated code - could be extracted
    print(f"\n{'='*60}")
    print(f"Stock Comparison: {ticker1} vs {ticker2}")
    print(f"{'='*60}")
    
    print(f"\n{ticker1}:")
    print(f"  Name: {info1.get('shortName', 'N/A')}")
    print(f"  Price: ${info1.get('currentPrice', 'N/A')}")
    print(f"  Market Cap: ${info1.get('marketCap', 'N/A'):,}")
    print(f"  P/E Ratio: {info1.get('trailingPE', 'N/A')}")
    print(f"  52-Week High: ${info1.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"  52-Week Low: ${info1.get('fiftyTwoWeekLow', 'N/A')}")
    
    print(f"\n{ticker2}:")
    print(f"  Name: {info2.get('shortName', 'N/A')}")
    print(f"  Price: ${info2.get('currentPrice', 'N/A')}")
    print(f"  Market Cap: ${info2.get('marketCap', 'N/A'):,}")
    print(f"  P/E Ratio: {info2.get('trailingPE', 'N/A')}")
    print(f"  52-Week High: ${info2.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"  52-Week Low: ${info2.get('fiftyTwoWeekLow', 'N/A')}")


# FEATURE GAP: This function is incomplete - needs AI integration
def analyze_stock(ticker):
    """
    AI-powered stock analysis.
    
    TODO: Implement this using OpenAI/Azure to:
    1. Summarize recent news sentiment
    2. Generate investment thesis
    3. Identify key risks
    """
    print(f"AI analysis for {ticker} is not yet implemented.")
    print("This is a feature generation exercise!")
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Stock Price Analyzer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Price command
    price_parser = subparsers.add_parser("price", help="Get current stock price")
    price_parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Get price history")
    history_parser.add_argument("ticker", help="Stock ticker symbol")
    history_parser.add_argument("--days", type=int, default=30, help="Number of days")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two stocks")
    compare_parser.add_argument("ticker1", help="First stock ticker")
    compare_parser.add_argument("ticker2", help="Second stock ticker")
    
    # Analyze command (incomplete)
    analyze_parser = subparsers.add_parser("analyze", help="AI-powered analysis")
    analyze_parser.add_argument("ticker", help="Stock ticker symbol")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # REFACTORING OPPORTUNITY: This could use a command pattern
    if args.command == "price":
        result = fetch_stock_price(args.ticker)
        print(f"\n{result['name']} ({result['symbol']})")
        print(f"  Current Price: ${result['price']:.2f}")
        print(f"  Change: {result['change']:.2f}%")
        
    elif args.command == "history":
        hist = fetch_history(args.ticker, args.days)
        print(f"\nPrice history for {args.ticker} (last {args.days} days):")
        print(hist.tail(10).to_string())
        
    elif args.command == "compare":
        display_comparison(args.ticker1, args.ticker2)
        
    elif args.command == "analyze":
        analyze_stock(args.ticker)


if __name__ == "__main__":
    main()
