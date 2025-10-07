from twilio.rest import Client
from dotenv import load_dotenv
import os
from utilities.logger import Logger

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
            Logger.log("MessageClient initialized", component="MESSAGE")

    def send_message(self, msg: str):
        try:
            message = self.client.messages.create(
                body = msg,
                from_=self.from_number,
                to=self.to_number,
            )
            Logger.log("Message sent", component="MESSAGE", context={"sid": message.sid})
            return message.sid
        except Exception as e:
            Logger.error(f"Failed to send message: {e}", component="MESSAGE")
            raise
    
    @staticmethod
    def send(msg: str):
        return MessageClient().send_message(msg)