#!/bin/bash
# Setup script for Linux/Mac systems

echo "Setting up stock analysis cron job..."

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create log directory
mkdir -p "$SCRIPT_DIR/logs"

# Create cron entry
CRON_ENTRY="30 12 * * 1-5 cd $SCRIPT_DIR && /usr/bin/python3 main_workflow.py >> logs/cron.log 2>&1"

# Add to cron
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "Cron job added successfully!"
echo "The script will run at 12:30 PM on weekdays"
echo "Check logs in: $SCRIPT_DIR/logs/cron.log"

# Create environment variables file template
cat > .env.template << EOF
# API Keys - Copy this to .env and fill in your actual keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
FMP_API_KEY=your_fmp_key_here
MARKETAUX_API_KEY=your_marketaux_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
# TWILIO_ACCOUNT_SID=your_twilio_sid
# TWILIO_AUTH_TOKEN=your_twilio_token
# TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
# YOUR_WHATSAPP_NUMBER=whatsapp:+919876543210
STOCK_WATCHLIST=AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,META
EOF

echo "Environment template created as .env.template"
echo "Copy it to .env and add your API keys"
