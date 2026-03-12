import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Memoria por usuario
conversation_history = {}

@app.route("/", methods=["GET"])
def home():
    return "Bot activo", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "")
    user_id = request.form.get("From", "")

    # Iniciar historial si es nuevo usuario
    if user_id not in conversation_history:
        conversation_history[user_id] = [
            {"role": "system", "content": "Eres un asistente amigable que responde en el mismo idioma del usuario. Recuerdas el contexto de la conversación."}
        ]

    # Agregar mensaje del usuario
    conversation_history[user_id].append(
        {"role": "user", "content": incoming_msg}
    )

    # Llamar a Groq con historial
    chat = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history[user_id]
    )

    ai_response = chat.choices[0].message.content

    # Guardar respuesta en historial
    conversation_history[user_id].append(
        {"role": "assistant", "content": ai_response}
    )

    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
    
