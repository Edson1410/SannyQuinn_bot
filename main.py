import requests
import os
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "7782223425:AAH9TEiLLppRxeK2jMsfJVT7zbid8K1KaoQ"
OPENROUTER_KEY = "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"

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_ai_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/mixtral-8x7b",
        "messages": [
            {"role": "system", "content": "Você é Sanny Quinn, uma companheira afetuosa e realista."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except:
        return "Desculpe, não consegui responder agora"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")
        if user_text:
            reply = get_ai_response(user_text)
            send_message(chat_id, reply)
    return {"ok": True}

@app.route("/", methods=["GET"])
def home():
    return "💖 Sanny Quinn está online!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ ESSENCIAL no Render
    app.run(host="0.0.0.0", port=port)
