import requests
import json
import random
import time
import schedule
import os
from dotenv import load_dotenv

# --- 1. CARREGAR CHAVES DE SEGURANÇA ---
load_dotenv() 

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") 

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("ERRO: O Token do Bot ou o Chat ID do Telegram não foram carregados.")
    exit()
    
# --- 2. FUNÇÃO DE ENVIO PARA O TELEGRAM ---
def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown' 
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() 
        print(f"[INFO] Mensagem enviada com sucesso às {time.strftime('%H:%M:%S')}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao enviar mensagem para o Telegram: {e}")

# --- 3. FUNÇÃO DE LÓGICA DO PALPITE (SIMULAÇÃO) ---
def gerar_palpite_diario():
    print(f"[INFO] Gerando palpite às {time.strftime('%H:%M:%S')}...")
    
    jogos_ficticios = [
        ("Flamengo", "Fluminense"),
        ("Corinthians", "São Paulo"),
        ("Real Madrid", "Barcelona"),
    ]
    
    time_casa, time_fora = random.choice(jogos_ficticios)
    chance_casa = random.randint(50, 90)
    
    if chance_casa > 60:
        palpite = f"Vitória simples do {time_casa}"
        probabilidade = f"{chance_casa}%"
    else:
        palpite = f"Mais de 2.5 gols"
        probabilidade = "Alta"
        
    mensagem = f"""
⚽ *PALPITE DO DIA - {time.strftime('%d/%m')}* ⚽
        
*Jogo:* {time_casa} vs {time_fora}
*Aposta Sugerida:* {palpite}
*Probabilidade de Acerto:* {probabilidade}
        
_Lembre-se: Aposte com responsabilidade._
"""
    enviar_mensagem_telegram(mensagem)
    
# --- 4. AGENDAMENTO DOS PALPITES ---
schedule.every().day.at("10:00").do(generar_palpite_diario)
schedule.every().day.at("18:00").do(generar_palpite_diario)
print("[INFO] Bot de Palpites Agendado e Iniciado.")

# --- LOOP PRINCIPAL ---
while True:
    schedule.run_pending()
    time.sleep(1)
