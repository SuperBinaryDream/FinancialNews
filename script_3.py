# Create the main workflow orchestrator
main_workflow = '''
#!/usr/bin/env python3
"""
Daily Stock Analysis Workflow
Runs weekdays to analyze your stock watchlist and send alerts
"""

import os
import sys
import json
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any

# Import our custom modules
from financial_analyzer import FinancialAnalyzer
from telegram_notifier import TelegramNotifier
# from whatsapp_notifier import WhatsAppNotifier  # Uncomment if using WhatsApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class StockAnalysisWorkflow:
    def __init__(self):
        self.analyzer = FinancialAnalyzer()
        self.telegram = TelegramNotifier()
        # self.whatsapp = WhatsAppNotifier()  # Uncomment if using WhatsApp
        
        # Load watchlist from environment or config
        self.watchlist = self.load_watchlist()
        
    def load_watchlist(self) -> List[str]:
        """Load stock watchlist from environment variable or config file"""
        # Option 1: From environment variable (comma-separated)
        env_watchlist = os.getenv('STOCK_WATCHLIST', '')
        if env_watchlist:
            return [stock.strip().upper() for stock in env_watchlist.split(',')]
        
        # Option 2: From config file
        try:
            with open('config/watchlist.json', 'r') as f:
                config = json.load(f)
                return config.get('stocks', [])
        except FileNotFoundError:
            # Default watchlist if no config found
            logger.warning("No watchlist configured, using default stocks")
            return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    def is_market_day(self) -> bool:
        """Check if today is a market trading day (weekday)"""
        today = datetime.now()
        # Monday = 0, Sunday = 6
        return today.weekday() < 5  # Monday to Friday
    
    def filter_important_updates(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter stocks with important updates (earnings, upgrades/downgrades)"""
        important = []
        
        for analysis in analyses:
            symbol = analysis['symbol']
            has_important_update = False
            
            # Check for upcoming earnings (within 7 days)
            earnings = analysis.get('earnings')
            if earnings:
                earnings_date = earnings.get('date')
                if earnings_date:
                    try:
                        earnings_dt = datetime.strptime(earnings_date, '%Y-%m-%d')
                        days_until = (earnings_dt - datetime.now()).days
                        if 0 <= days_until <= 7:
                            has_important_update = True
                            logger.info(f"{symbol}: Earnings in {days_until} days")
                    except ValueError:
                        pass
            
            # Check for recent analyst upgrades/downgrades
            recs = analysis.get('analyst_recs', [])
            for rec in recs[:2]:  # Check last 2 recommendations
                rec_date = rec.get('date', '')
                if rec_date:
                    try:
                        rec_dt = datetime.strptime(rec_date, '%Y-%m-%d')
                        if (datetime.now() - rec_dt).days <= 3:  # Within 3 days
                            has_important_update = True
                            grade = rec.get('newGrade', '')
                            logger.info(f"{symbol}: Recent analyst update - {grade}")
                    except ValueError:
                        pass
            
            # Check for significant price movement (>5%)
            price_data = analysis.get('price_data', {}).get('Global Quote', {})
            if price_data:
                change_pct_str = price_data.get('10. change percent', '0%')
                try:
                    change_pct = float(change_pct_str.replace('%', ''))
                    if abs(change_pct) > 5.0:
                        has_important_update = True
                        logger.info(f"{symbol}: Significant price movement - {change_pct}%")
                except ValueError:
                    pass
            
            # Check for important news keywords
            news_items = analysis.get('news', [])
            important_keywords = ['earnings', 'upgrade', 'downgrade', 'acquisition', 'merger', 'lawsuit', 'fda approval']
            for news in news_items[:3]:
                title_lower = news.get('title', '').lower()
                if any(keyword in title_lower for keyword in important_keywords):
                    has_important_update = True
                    logger.info(f"{symbol}: Important news - {news.get('title', '')[:50]}")
                    break
            
            if has_important_update:
                important.append(analysis)
        
        return important
    
    def run_analysis(self) -> bool:
        """Run the complete analysis workflow"""
        try:
            logger.info("Starting daily stock analysis workflow")
            
            # Check if it's a market day
            if not self.is_market_day():
                logger.info("Market is closed today, skipping analysis")
                return True
            
            # Analyze all stocks in watchlist
            logger.info(f"Analyzing {len(self.watchlist)} stocks: {', '.join(self.watchlist)}")
            all_analyses = self.analyzer.analyze_watchlist(self.watchlist)
            
            if not all_analyses:
                logger.error("No analysis data retrieved")
                return False
            
            # Filter for important updates
            important_updates = self.filter_important_updates(all_analyses)
            
            # Generate summary
            if important_updates:
                summary = self.analyzer.generate_summary(important_updates)
                summary = "🚨 *IMPORTANT STOCK UPDATES* 🚨\\n\\n" + summary
                logger.info(f"Found {len(important_updates)} stocks with important updates")
            else:
                # Send brief summary even if no major updates
                summary = f"📊 *Daily Market Check* - {datetime.now().strftime('%Y-%m-%d')}\\n\\n"
                summary += "✅ No major updates for your watchlist today.\\n"
                summary += f"Monitored: {', '.join(self.watchlist)}"
                logger.info("No major updates found, sending brief summary")
            
            # Send notifications
            success = self.send_notifications(summary)
            
            # Save results for debugging
            self.save_results(all_analyses)
            
            logger.info("Workflow completed successfully")
            return success
            
        except Exception as e:
            error_msg = f"Workflow failed: {str(e)}"
            logger.error(error_msg)
            
            # Send error notification
            self.send_notifications(f"❌ Stock Analysis Error\\n\\n{error_msg}")
            return False
    
    def send_notifications(self, message: str) -> bool:
        """Send notifications via configured channels"""
        success = True
        
        # Send via Telegram (free)
        try:
            if self.telegram.send_message(message):
                logger.info("Telegram notification sent successfully")
            else:
                logger.error("Failed to send Telegram notification")
                success = False
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            success = False
        
        # Send via WhatsApp (uncomment if using)
        # try:
        #     if self.whatsapp.send_message(message):
        #         logger.info("WhatsApp notification sent successfully")
        #     else:
        #         logger.error("Failed to send WhatsApp notification")
        #         success = False
        # except Exception as e:
        #     logger.error(f"WhatsApp error: {e}")
        #     success = False
        
        return success
    
    def save_results(self, analyses: List[Dict[str, Any]]) -> None:
        """Save analysis results to file for debugging"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"results/analysis_{timestamp}.json"
        
        # Create results directory if it doesn't exist
        os.makedirs('results', exist_ok=True)
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'watchlist': self.watchlist,
                    'analyses': analyses
                }, f, indent=2)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

def main():
    """Main entry point"""
    workflow = StockAnalysisWorkflow()
    success = workflow.run_analysis()
    
    if success:
        print("✅ Stock analysis workflow completed successfully")
        sys.exit(0)
    else:
        print("❌ Stock analysis workflow failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

with open('main_workflow.py', 'w') as f:
    f.write(main_workflow)

print("✅ Created main_workflow.py")
print("\nMain workflow features:")
print("- Weekday-only execution (market days)")
print("- Intelligent filtering for important updates")
print("- Multi-channel notifications")
print("- Error handling and logging")
print("- Results archiving for debugging")