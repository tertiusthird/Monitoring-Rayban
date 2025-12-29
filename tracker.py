import requests
from bs4 import BeautifulSoup
import os

# Configurações do Monitor
URL = "https://www.ray-ban.com/brazil/oculos-de-sol/RB2140%20UNISEX%20wayfarer%20classic-preto/805289126577"
PRECO_ALVO = 750
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Busca o preço no site da Ray-Ban via meta tag
        price_tag = soup.find("meta", property="product:price:amount")
        
        if price_tag:
            price = float(price_tag["content"])
            print(f"Preço actual encontrado: R$ {price}")
            
            if price <= PRECO_ALVO:
                send_notification(price)
            else:
                print("Preço ainda acima do alvo. Sem alerta.")
        else:
            print("Erro: Não foi possível ler o preço no site.")
            
    except Exception as e:
        print(f"Erro na execução: {e}")

def send_notification(price):
    msg = f"🚨 PROMOÇÃO RAY-BAN!\n\nO Wayfarer baixou para R$ {price}!\nLink: {URL}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(send_url)

if __name__ == "__main__":
    check_price()
