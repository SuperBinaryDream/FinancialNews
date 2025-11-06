
import requests
import os

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')  # Your personal chat ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message: str) -> bool:
        """Send message via Telegram"""
        if not (self.bot_token and self.chat_id):
            raise RuntimeError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown'  # Enable markdown formatting
        }

        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
            return False

    def send_document(self, file_path: str, caption: str = "") -> bool:
        """Send document via Telegram"""
        if not (self.bot_token and self.chat_id):
            raise RuntimeError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        url = f"{self.base_url}/sendDocument"

        try:
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                response = requests.post(url, files=files, data=data)
                return response.status_code == 200
        except Exception as e:
            print(f"Failed to send document: {e}")
            return False

# How to get your Chat ID:
# 1. Send a message to your bot
# 2. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
# 3. Look for "chat":{"id": YOUR_CHAT_ID}

if __name__ == "__main__":
    notifier = TelegramNotifier()
    test_message = "🤖 Stock Analysis Bot is now active!\n\nYou will receive daily market updates here."
    success = notifier.send_message(test_message)
    print(f"Test message sent: {success}")
