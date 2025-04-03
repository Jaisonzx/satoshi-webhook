from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import ChatInviteLink
import requests
import time

# Configuração Telegram
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"
chat_id = -1002531479445
webhook_n8n = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# Inicializa o client global (mas não conecta ainda)
app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)

# Flask app
app = Flask(__name__)

@app.route("/gera-link", methods=["POST"])
def gerar_link():
    try:
        print("🚀 Iniciando geração de link...")

        app_pyro.start()

        link: ChatInviteLink = app_pyro.create_chat_invite_link(
            chat_id=chat_id,
            expire_date=int(time.time()) + 86400,
            member_limit=1,
            name="Aprovação ADM"
        )

        app_pyro.stop()

        print("✅ Link gerado:", link.invite_link)

        payload = {
            "nome": "Aprovação ADM",
            "link": link.invite_link
        }

        # Envia para o webhook
        requests.post(webhook_n8n, json=payload)

        return jsonify({"status": "link enviado com sucesso"}), 200

    except Exception as e:
        print("❌ Erro:", str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
