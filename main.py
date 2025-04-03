from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import ChatInviteLink
import requests
import time

# CONFIGURAÇÕES DO TELEGRAM
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"
chat_id = -1002531479445  # Canal privado
webhook_n8n = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# INICIALIZA O TELEGRAM
app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)

# INICIALIZA O FLASK
app = Flask(__name__)

@app.route("/gera-link", methods=["POST"])
def gerar_link():
    try:
        with app_pyro:
            link: ChatInviteLink = app_pyro.create_chat_invite_link(
                chat_id=chat_id,
                expire_date=int(time.time()) + 86400,  # 1 dia
                member_limit=1,
                name="Aprovação ADM"
            )

            payload = {
                "nome": "Aprovação ADM",
                "link": link.invite_link
            }

            print("✅ Link criado:", link.invite_link)

            # Envia para o webhook do n8n
            requests.post(webhook_n8n, json=payload)

            return jsonify({"status": "link enviado"}), 200

    except Exception as e:
        print("❌ Erro:", str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
