from mysite.settings import ACCOUNT_SID, AUTH_TOKEN, PHONE_SENDER
from twilio.rest import Client

class SMS():
  def __init__(self, request):
    self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
  def message(self, body, receiver):
    message = self.client.messages.create( body = body, from_=PHONE_SENDER, to =receiver)
    print(message.sid)