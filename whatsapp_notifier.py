
import os
from twilio.rest import Client

class WhatsAppNotifier:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')  # e.g., 'whatsapp:+14155238886'
        self.to_whatsapp = os.getenv('YOUR_WHATSAPP_NUMBER')     # e.g., 'whatsapp:+919876543210'
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, message: str) -> bool:
        """Send message via WhatsApp"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_whatsapp,
                to=self.to_whatsapp
            )
            print(f"Message sent with SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
            return False

if __name__ == "__main__":
    notifier = WhatsAppNotifier()
    test_message = "🤖 Stock Analysis Bot Test\n\nThis is a test message from your automated stock analysis system."
    success = notifier.send_message(test_message)
    print(f"Test WhatsApp message sent: {success}")
