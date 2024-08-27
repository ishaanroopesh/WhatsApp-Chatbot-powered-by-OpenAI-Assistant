from twilio.rest import Client

account_sid = #Account ID
auth_token = #Authorisation token here
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+XXXXXXXXXXXX' #ex :- +911234567890
)

print(message.sid)
