import requests
import schedule
import time

TOKEN = "COLOQUE_SEU_TOKEN_AQUI"
CHAT_ID = "COLOQUE_SEU_CHAT_ID_AQUI"

def enviar_palpite():
    mensagem = "💡 Palpite do dia: Vitória do time da casa!"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem}
    requests.get(url, params=params)

# Agenda o envio diário
schedule.every().day.at("10:00").do(enviar_palpite)

print("✅ Bot iniciado...")

while True:
    schedule.run_pending()
    time.sleep(1)
