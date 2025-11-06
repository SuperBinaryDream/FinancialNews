# Windows Task Scheduler setup script
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
