import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "")
    
    # 1. Pedir respuesta a la IA
    chat = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": incoming_msg}]
    )
    
    ai_response = chat.choices[0].message.content

    # 2. Enviar respuesta de vuelta a WhatsApp
    resp = MessagingResponse()
    resp.message(ai_response)
    
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
    