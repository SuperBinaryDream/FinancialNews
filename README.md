# Automated Stock Analysis & Alert System

This system automatically analyzes your stock watchlist every weekday and sends you important updates via Telegram or WhatsApp.

## Features
- 📊 Daily earnings calendar monitoring
- 📈 Analyst recommendation tracking  
- 📰 Important news filtering
- 💰 Price movement alerts (>5% changes)
- 🤖 Automated Telegram/WhatsApp notifications
- ☁️ Free cloud execution via GitHub Actions
- 📝 Comprehensive logging and error handling

## Quick Start

### 1. Get Free API Keys
- **Alpha Vantage**: Visit https://www.alphavantage.co/support/#api-key (25 free calls/day)
- **Financial Modeling Prep**: Visit https://financialmodelingprep.com/developer/docs (250 free calls/day)  
- **Marketaux**: Visit https://www.marketaux.com/ (100 free calls/day)

### 2. Set Up Telegram Bot
1. Open Telegram and message @BotFather
2. Send `/newbot` and follow instructions
3. Save your bot token
4. Message your bot, then visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. Find your chat ID in the response

### 3. Configure Your Watchlist
Edit `config/watchlist.json` or set `STOCK_WATCHLIST` environment variable

### 4. Choose Deployment Method

#### Option A: GitHub Actions (Free, Recommended)
1. Create GitHub repository
2. Push all files to repository  
3. Go to Settings > Secrets and Actions
4. Add your API keys as repository secrets:
   - `ALPHA_VANTAGE_API_KEY`
   - `FMP_API_KEY` 
   - `MARKETAUX_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. The workflow runs automatically at 12:00 PM IST on weekdays

#### Option B: Local Cron Job
1. Copy `.env.template` to `.env` and add your API keys
2. Run `./setup_cron.sh` (Linux/Mac) or `setup_windows.ps1` (Windows)
3. The script runs at 12:30 PM on weekdays

## File Structure
```
stock-analysis-bot/
├── main_workflow.py           # Main orchestration script
├── financial_analyzer.py      # Stock analysis logic
├── telegram_notifier.py       # Telegram messaging
├── whatsapp_notifier.py      # WhatsApp messaging (optional)
├── requirements.txt          # Python dependencies
├── config/
│   └── watchlist.json       # Your stock watchlist
├── .github/workflows/
│   └── stock-analysis.yml   # GitHub Actions workflow
├── setup_cron.sh            # Linux/Mac cron setup
├── setup_windows.ps1        # Windows task scheduler setup
└── .env.template            # Environment variables template
```

## Sample Telegram Alert
```
🚨 IMPORTANT STOCK UPDATES 🚨

🔹 AAPL
   Price: $175.43 (+3.2%)
   📅 Earnings: 2024-01-25
   📈 Latest: Buy by Morgan Stanley
   📰 News: Apple reports strong iPhone sales...

🔹 MSFT  
   Price: $420.15 (-2.1%)
   📈 Latest: Upgrade to Strong Buy by Goldman Sachs
   📰 News: Microsoft Azure sees 30% growth...
```

## API Limits & Costs
- **GitHub Actions**: 2000 free minutes/month for private repos, unlimited for public
- **Alpha Vantage**: 25 free API calls/day  
- **Financial Modeling Prep**: 250 free API calls/day
- **Marketaux**: 100 free API calls/day
- **Telegram**: Completely free
- **WhatsApp (Twilio)**: $15 free credits, then $0.005/message

## Customization
- Edit `config/config.json` to adjust analysis settings
- Modify `filter_important_updates()` in `main_workflow.py` for custom filtering
- Add more notification channels by creating new notifier classes

## Troubleshooting
1. Check `stock_analysis.log` for error details
2. Verify API keys are correct and have remaining quota
3. Ensure Telegram bot token and chat ID are valid  
4. Test individual components with `python financial_analyzer.py`

## Security Notes
- Never commit API keys to version control
- Use GitHub Secrets for cloud deployment
- Use environment variables or .env files for local deployment
- Keep your Telegram bot token private

## License
MIT License - feel free to modify and distribute
