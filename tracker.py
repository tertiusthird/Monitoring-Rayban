import requests
from bs4 import BeautifulSoup
import os

# Configurações via Variáveis de Ambiente
URL = "https://www.ray-ban.com/brazil/oculos-de-sol/RB2140%20UNISEX%20wayfarer%20classic-preto/805289126577"
# Agora o preço vem das configurações do GitHub (ou 750 por padrão)
PRECO_ALVO = float(os.environ.get('PRECO_ALVO', 750))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        price_tag = soup.find("meta", property="product:price:amount")
        
        if price_tag:
            current_price = float(price_tag["content"])
            print(f"DEBUG: Preço no site: R$ {current_price} | Alvo: R$ {PRECO_ALVO}")
            
            if current_price <= PRECO_ALVO:
                send_notification(current_price)
            else:
                print("Preço ainda acima do alvo.")
        else:
            print("Erro: Preço não encontrado na página.")
            
    except Exception as e:
        print(f"Erro na execução: {e}")

def send_notification(price):
    msg = f"🚨 TESTE DE PREÇO RAY-BAN!\n\nO valor atual é R$ {price}, que está abaixo do seu alvo de R$ {PRECO_ALVO}!\n\nLink: {URL}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(send_url)

if __name__ == "__main__":
    check_price()
