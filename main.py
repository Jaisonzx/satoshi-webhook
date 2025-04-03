from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import ChatInviteLink
from datetime import datetime, timedelta
import requests
import threading

# CONFIG
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"
chat_id = -1002531479445
nome_do_link = "Aprovação ADM"
webhook_destino = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# FLASK APP
app = Flask(__name__)

@app.route("/gera-link", methods=["POST"])
def gerar_link():
    try:
        print("🚀 Criando link de convite...")

        expire_date = datetime.utcnow() + timedelta(days=1)

        # Cria link direto (client já está ativo no thread principal)
        link: ChatInviteLink = app_pyro.create_chat_invite_link(
            chat_id=chat_id,
            expire_date=expire_date,
            member_limit=1,
            name=nome_do_link
        )

        print(f"✅ Link gerado: {link.invite_link}")

        payload = {
            "nome": nome_do_link,
            "link": link.invite_link
        }

        resposta = requests.post(webhook_destino, json=payload)
        print("📨 Enviado para webhook. Código:", resposta.status_code)

        return jsonify({"status": "ok", "link": link.invite_link}), 200

    except Exception as e:
        print("❌ ERRO:", str(e))
        return jsonify({"erro": str(e)}), 500

def start_flask():
    print("🟢 Servidor Flask rodando em http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # INICIA O PYROGRAM CLIENT NO THREAD PRINCIPAL
    app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)
    app_pyro.start()

    # INICIA O FLASK EM UMA THREAD SEPARADA
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
