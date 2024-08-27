from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
from assistants_quickstart import generate_response

app = Flask(__name__)

def remove_citations(text):
    return re.sub(r'【\d+:\d+†.*?】', '', text)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    response = MessagingResponse()
    incoming_msg = request.form.get('Body') # Content of the message
    wa_id = request.form.get('From')  # WhatsApp sender ID
    name = "ABCD" #Enter your name here or extract it from the message

    print(f"Received message from {wa_id}, {name}: {incoming_msg}")

    reply = remove_citations(generate_response(incoming_msg, wa_id, name))
    response.message(reply)

    print(f"Response: {reply}")

    # response.message("Hello there!")
    return str(response)

if __name__ == "__main__":
    app.run(port=8080)
