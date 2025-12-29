import requests
from bs4 import BeautifulSoup
import os
import json
import time

# Configurações
URL = "https://www.ray-ban.com/brazil/oculos-de-sol/RB2140%20UNISEX%20wayfarer%20classic-preto/805289126577"
PRECO_ALVO = float(os.environ.get('PRECO_ALVO', 750))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def check_price():
    # Sessão para manter cookies e parecer humano
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }
    
    print(f"--- Iniciando Tentativa de Camuflagem v3.0 ---")
    try:
        # Primeiro faz um "warm-up" na home para pegar cookies
        print("DEBUG: Simulando acesso à home...")
        session.get("https://www.ray-ban.com/brazil", headers=headers, timeout=15)
        time.sleep(2) # Espera 2 segundos como um humano
        
        # Agora tenta acessar o produto
        print(f"DEBUG: Acedendo ao produto...")
        response = session.get(URL, headers=headers, timeout=20)
        
        print(f"DEBUG: Status final: {response.status_code}")
        
        if response.status_code == 403:
            print("ERRO 403: O site ainda nos bloqueou. IP do GitHub está marcado.")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        price = None

        # Procura nos scripts JSON-LD (mais difícil de esconder do que meta tags)
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            if not script.string: continue
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and 'offers' in data:
                    offers = data['offers']
                    if isinstance(offers, dict):
                        price = float(offers.get('price'))
                        break
                    elif isinstance(offers, list):
                        price = float(offers[0].get('price'))
                        break
            except:
                continue

        if price:
            print(f"SUCESSO! Preço encontrado: R$ {price}")
            if price <= PRECO_ALVO:
                send_notification(price)
            else:
                print(f"Preço R$ {price} ainda acima do alvo R$ {PRECO_ALVO}")
        else:
            print("ERRO: Não encontrei o preço no HTML, apesar da conexão 200.")
            
    except Exception as e:
        print(f"ERRO DE SISTEMA: {e}")

def send_notification(price):
    msg = f"🚨 BAIXOU O PREÇO!\n\nRay-Ban Wayfarer: R$ {price}\nLink: {URL}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(send_url)

if __name__ == "__main__":
    check_price()
