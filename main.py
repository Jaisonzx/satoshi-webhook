from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import ChatInviteLink
import requests
from datetime import datetime, timedelta
import threading
import asyncio

# CONFIGS
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"
chat_id = -1002531479445
nome_do_link = "Aprovação ADM"
webhook_destino = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# FLASK
app = Flask(__name__)

# CLIENTE PYROGRAM GLOBAL
app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)
pyro_loop = asyncio.new_event_loop()

def start_pyrogram():
    asyncio.set_event_loop(pyro_loop)
    app_pyro.run()

@app.route("/gera-link", methods=["POST"])
def gerar_link():
    try:
        print("🚀 Criando link de convite...")

        expire_date = datetime.utcnow() + timedelta(days=1)

        future = asyncio.run_coroutine_threadsafe(
            app_pyro.create_chat_invite_link(
                chat_id=chat_id,
                expire_date=expire_date,
                member_limit=1,
                name=nome_do_link
            ),
            pyro_loop
        )

        link: ChatInviteLink = future.result()

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
    print("🟢 Servidor Flask em execução em http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=start_pyrogram).start()
    threading.Thread(target=start_flask).start()
