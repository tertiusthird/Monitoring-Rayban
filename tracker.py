import requests
from bs4 import BeautifulSoup
import os
import json

# Configurações
URL = "https://www.ray-ban.com/brazil/oculos-de-sol/RB2140%20UNISEX%20wayfarer%20classic-preto/805289126577"
PRECO_ALVO = float(os.environ.get('PRECO_ALVO', 750))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def check_price():
    # Cabeçalhos mais complexos para fingir ser um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com.br/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    
    print(f"--- Iniciando Verificação v2.0 ---")
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        print(f"DEBUG: Status da Conexão: {response.status_code}")
        
        if response.status_code != 200:
            print(f"ERRO: Site retornou status {response.status_code}. Provável bloqueio.")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        price = None

        # TENTATIVA 1: Meta tag (Schema.org)
        price_tag = soup.find("meta", property="product:price:amount")
        if price_tag:
            price = float(price_tag["content"])
            print("INFO: Preço encontrado via Meta Tag.")

        # TENTATIVA 2: JSON-LD (Scripts de dados estruturados)
        if not price:
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts:
                try:
                    data = json.loads(script.string)
                    # Procura em ofertas de produtos
                    if isinstance(data, dict) and data.get('@type') == 'Product':
                        offers = data.get('offers', {})
                        if isinstance(offers, dict):
                            price = float(offers.get('price'))
                            print("INFO: Preço encontrado via JSON-LD (Product).")
                            break
                        elif isinstance(offers, list) and len(offers) > 0:
                            price = float(offers[0].get('price'))
                            print("INFO: Preço encontrado via JSON-LD (Offer List).")
                            break
                except:
                    continue

        if price:
            print(f"SUCESSO: Preço: R$ {price} | Alvo: R$ {PRECO_ALVO}")
            if price <= PRECO_ALVO:
                send_notification(price)
            else:
                print("STATUS: Preço ainda acima do esperado.")
        else:
            print("ERRO: Não foi possível localizar o preço pelos métodos conhecidos.")
            
    except Exception as e:
        print(f"ERRO FATAL: {e}")

def send_notification(price):
    msg = f"🚨 PROMOÇÃO RAY-BAN!\n\nO valor baixou para R$ {price}!\n\nLink: {URL}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(send_url)

if __name__ == "__main__":
    check_price()
