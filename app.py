import os
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse

from groq import Groq

app = Flask(__name__)

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/webhook", methods=["POST"])

def webhook():

    incoming_msg = request.form.get("Body", "")

    

    chat = groq_client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[{"role": "user", "content": incoming_msg}]

    )

    respuesta = chat.choices[0].message.content

    resp = MessagingResponse()

    resp.message(respuesta)

    return str(resp)

if __name__ == "__main__":

    app.run(port=5000, debug=True)