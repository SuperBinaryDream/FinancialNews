
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class FinancialAnalyzer:
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.fmp_key = os.getenv('FMP_API_KEY')
        self.marketaux_key = os.getenv('MARKETAUX_API_KEY')

    

    def get_earnings_calendar(self, symbol: str) -> Dict[str, Any]:
        """Get upcoming earnings for a stock"""
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar"
        params = {
            'apikey': self.fmp_key,
            'from': datetime.now().strftime('%Y-%m-%d'),
            'to': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }

        response = requests.get(url, params=params)
        data = response.json()
        if not isinstance(data, list):
            return None

        # Filter for specific symbol
        earnings = [item for item in data if item.get('symbol') == symbol]
        return earnings[0] if earnings else None

    def get_analyst_recommendations(self, symbol: str) -> Dict[str, Any]:
        """Get latest analyst recommendations"""
        url = f"https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{symbol}"
        params = {'apikey': self.fmp_key, 'limit': 10}

        response = requests.get(url, params=params)
        data = response.json()
        if not isinstance(data, list):
            return []
        return data

    def get_stock_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Get recent news for a stock"""
        url = "https://api.marketaux.com/v1/news/all"
        params = {
            'api_token': self.marketaux_key,
            'symbols': symbol,
            'filter_entities': 'true',
            'limit': 5,
            'published_after': (datetime.now() - timedelta(days=1)).isoformat()
        }

        response = requests.get(url, params=params)
        data = response.json()
        if isinstance(data, dict):
            return data.get('data', [])
        return []

    def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get current stock price and basic info"""
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.alpha_vantage_key
        }

        response = requests.get(url, params=params)
        data = response.json()
        if not isinstance(data, dict):
            return {}
        return data

    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Comprehensive analysis of a single stock"""
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'price_data': self.get_stock_price(symbol),
            'earnings': self.get_earnings_calendar(symbol),
            'analyst_recs': self.get_analyst_recommendations(symbol)[:3],  # Latest 3
            'news': self.get_stock_news(symbol)
        }

        return analysis

    def analyze_watchlist(self, stocks: List[str]) -> List[Dict[str, Any]]:
        """Analyze all stocks in watchlist"""
        results = []

        for stock in stocks:
            try:
                analysis = self.analyze_stock(stock)
                results.append(analysis)
                # Rate limiting - respect API limits
                import time
                time.sleep(1)  # 1 second between calls
            except Exception as e:
                print(f"Error analyzing {stock}: {e}")

        return results

    def generate_summary(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate human-readable summary"""
        summary = f"📊 Daily Stock Analysis - {datetime.now().strftime('%Y-%m-%d')}\n\n"

        for analysis in analyses:
            symbol = analysis['symbol']
            summary += f"🔹 *{symbol}*\n"

            # Price info
            price_data = analysis.get('price_data', {}).get('Global Quote', {})
            if price_data:
                price = price_data.get('05. price', 'N/A')
                change_pct = price_data.get('10. change percent', 'N/A')
                summary += f"   Price: ${price} ({change_pct})\n"

            # Earnings
            earnings = analysis.get('earnings')
            if earnings:
                earnings_date = earnings.get('date', 'N/A')
                summary += f"   📅 Earnings: {earnings_date}\n"

            # Latest analyst recommendation
            recs = analysis.get('analyst_recs', [])
            if recs:
                latest_rec = recs[0]
                analyst = latest_rec.get('analystCompany', 'Unknown')
                rating = latest_rec.get('newGrade', 'N/A')
                summary += f"   📈 Latest: {rating} by {analyst}\n"

            # Important news
            news_items = analysis.get('news', [])
            important_news = [n for n in news_items if 'earnings' in n.get('title', '').lower() 
                             or 'upgrade' in n.get('title', '').lower() 
                             or 'downgrade' in n.get('title', '').lower()]

            if important_news:
                summary += f"   📰 News: {important_news[0]['title'][:50]}...\n"

            summary += "\n"

        return summary

# Sample usage and configuration
if __name__ == "__main__":
    # Sample configuration - you would load this from environment variables
    SAMPLE_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

    analyzer = FinancialAnalyzer()
    results = analyzer.analyze_watchlist(SAMPLE_WATCHLIST)
    summary = analyzer.generate_summary(results)
    print(summary)
