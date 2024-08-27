from twilio.rest import Client

account_sid = 'AC80e4218a2292d4467f4f03edda50e6fa'
auth_token = 'c3f98bbc445b71b52f3a9cb14ef52c05'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+919902685178'
)

print(message.sid)