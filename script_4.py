# Create GitHub Actions workflow file
github_workflow = '''name: Daily Stock Analysis
on:
  schedule:
    # Run at 6:30 AM UTC (12:00 PM IST) on weekdays
    - cron: '30 6 * * 1-5'
  workflow_dispatch: # Allow manual trigger

jobs:
  stock-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests pandas python-telegram-bot twilio
        
    - name: Create config directories
      run: |
        mkdir -p config results
        
    - name: Create watchlist config
      run: |
        cat > config/watchlist.json << EOF
        {
          "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]
        }
        EOF
        
    - name: Run stock analysis
      env:
        ALPHA_VANTAGE_API_KEY: ${{ secrets.ALPHA_VANTAGE_API_KEY }}
        FMP_API_KEY: ${{ secrets.FMP_API_KEY }}
        MARKETAUX_API_KEY: ${{ secrets.MARKETAUX_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        # TWILIO_ACCOUNT_SID: ${{ secrets.TWILIO_ACCOUNT_SID }}
        # TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
        # TWILIO_WHATSAPP_NUMBER: ${{ secrets.TWILIO_WHATSAPP_NUMBER }}
        # YOUR_WHATSAPP_NUMBER: ${{ secrets.YOUR_WHATSAPP_NUMBER }}
      run: python main_workflow.py
      
    - name: Upload analysis results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: analysis-results
        path: |
          results/
          stock_analysis.log
        retention-days: 7
'''

# Create requirements.txt
requirements = '''requests>=2.28.0
pandas>=1.5.0
python-telegram-bot>=20.0
twilio>=8.0.0
'''

# Create .github/workflows directory structure
os.makedirs('.github/workflows', exist_ok=True)

with open('.github/workflows/stock-analysis.yml', 'w') as f:
    f.write(github_workflow)
    
with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("✅ Created GitHub Actions workflow")
print("Files created:")
print("- .github/workflows/stock-analysis.yml")
print("- requirements.txt")
print("\nSetup steps:")
print("1. Create GitHub repository")
print("2. Push these files to your repository")
print("3. Add API keys as GitHub Secrets (Settings > Secrets)")
print("4. The workflow runs automatically at 12:00 PM IST on weekdays")