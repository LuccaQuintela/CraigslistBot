from twilio.rest import Client
from dotenv import load_dotenv
import os

class MessageClient:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            load_dotenv()
            self.client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), )
            self.from_number = "whatsapp:+14155238886"
            self.to_number ='whatsapp:+16503363559'
            MessageClient._initialized = True

    def send_message(self, msg: str):
        message = self.client.messages.create(
            body = msg,
            from_=self.from_number,
            to=self.to_number,
        )
        return message.sid
    
    @staticmethod
    def send(msg: str):
        return MessageClient().send_message(msg)