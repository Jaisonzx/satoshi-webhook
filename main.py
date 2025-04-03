from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import ChatInviteLink
import requests
import time

# DADOS DA CONTA
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"

# CANAL
chat_id = -1002531479445  # Satoshi VIP Room
nome_do_link = "Aprovação ADM"

# WEBHOOK DE RETORNO
webhook_destino = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# TELEGRAM CLIENT
app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)

# FLASK SERVER
app = Flask(__name__)

@app.route("/gera-link", methods=["POST"])
def gerar_link():
    try:
        print("🚀 Criando link de convite...")

        app_pyro.start()

        link: ChatInviteLink = app_pyro.create_chat_invite_link(
            chat_id=chat_id,
            expire_date=int(time.time()) + 86400,  # 1 dia
            member_limit=1,
            name=nome_do_link
        )

        app_pyro.stop()

        print(f"✅ Link gerado: {link.invite_link}")

        # ENVIA PRO WEBHOOK
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

if __name__ == "__main__":
    print("🟢 Servidor iniciado em http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
