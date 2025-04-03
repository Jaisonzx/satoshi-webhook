from fastapi import FastAPI
from pyrogram import Client
from pyrogram.types import ChatInviteLink
from datetime import datetime, timedelta
import requests
import uvicorn

# CONFIG
api_id = 21884784
api_hash = "4bd2d2de4ed0d1662bbe341e95280e95"
session_name = "satoshi"
chat_id = -1002531479445
nome_do_link = "Aprovação ADM"
webhook_destino = "https://webhook.flowzin.site/webhook/satoshi-aprovação"

# APP FASTAPI
app = FastAPI()

# PYROGRAM CLIENT
app_pyro = Client(session_name, api_id=api_id, api_hash=api_hash)

@app.on_event("startup")
async def start_pyrogram():
    await app_pyro.start()

@app.on_event("shutdown")
async def stop_pyrogram():
    await app_pyro.stop()

@app.post("/gera-link")
async def gerar_link():
    try:
        print("🚀 Criando link de convite...")

        expire_date = datetime.utcnow() + timedelta(days=1)

        link: ChatInviteLink = await app_pyro.create_chat_invite_link(
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

        return {"status": "ok", "link": link.invite_link}

    except Exception as e:
        print("❌ ERRO:", str(e))
        return {"erro": str(e)}
