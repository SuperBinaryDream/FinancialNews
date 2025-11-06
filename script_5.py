# Create local automation scripts

# Linux/Mac cron setup script
cron_setup = '''#!/bin/bash
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
'''

# Windows Task Scheduler PowerShell script
windows_setup = '''# Windows Task Scheduler setup script
# Run this in PowerShell as Administrator

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "main_workflow.py"
$LogDir = Join-Path $ScriptDir "logs"

# Create log directory
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Create scheduled task
$Action = New-ScheduledTaskAction -Execute "python" -Argument $PythonScript -WorkingDirectory $ScriptDir
$Trigger = New-ScheduledTaskTrigger -Daily -At "12:30PM" -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Limited

Register-ScheduledTask -TaskName "StockAnalysis" -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Daily stock market analysis and alerts"

Write-Host "Scheduled task created successfully!"
Write-Host "Task: StockAnalysis"
Write-Host "Schedule: Daily at 12:30 PM on weekdays"
Write-Host "Remember to set up your API keys in environment variables or .env file"

# Create environment variables template
$EnvTemplate = @"
# API Keys - Set these as environment variables or create .env file
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
FMP_API_KEY=your_fmp_key_here
MARKETAUX_API_KEY=your_marketaux_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
STOCK_WATCHLIST=AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,META
"@

$EnvTemplate | Out-File -FilePath (Join-Path $ScriptDir ".env.template") -Encoding UTF8
Write-Host "Environment template created as .env.template"
'''

with open('setup_cron.sh', 'w') as f:
    f.write(cron_setup)

with open('setup_windows.ps1', 'w') as f:
    f.write(windows_setup)

# Make the Linux script executable
import stat
os.chmod('setup_cron.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

print("✅ Created local automation setup scripts")
print("Files created:")
print("- setup_cron.sh (Linux/Mac)")
print("- setup_windows.ps1 (Windows)")
print("\nFor local setup:")
print("Linux/Mac: Run ./setup_cron.sh")
print("Windows: Run setup_windows.ps1 in PowerShell as Administrator")