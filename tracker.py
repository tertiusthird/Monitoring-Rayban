import React, { useState } from 'react';
import { Bell, ShieldCheck, Mail, Send, Github, Code, ExternalLink, AlertCircle } from 'lucide-react';

const App = () => {
  const [threshold, setThreshold] = useState(750);
  const [activeTab, setActiveTab] = useState('setup');

  const productUrl = "https://www.ray-ban.com/brazil/oculos-de-sol/RB2140%20UNISEX%20wayfarer%20classic-preto/805289126577";

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Header */}
      <header className="bg-black text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-red-600 p-2 rounded">
              <ShieldCheck size={24} />
            </div>
            <h1 className="text-2xl font-bold tracking-tighter">RAY-BAN TRACKER</h1>
          </div>
          <div className="hidden md:flex gap-4 text-sm font-medium">
            <button onClick={() => setActiveTab('setup')} className={`hover:text-red-400 transition ${activeTab === 'setup' ? 'text-red-400' : ''}`}>Configuração</button>
            <button onClick={() => setActiveTab('code')} className={`hover:text-red-400 transition ${activeTab === 'code' ? 'text-red-400' : ''}`}>Código Python</button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6">
        {/* Banner de Status */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 mb-8 shadow-sm flex flex-col md:flex-row items-center gap-6">
          <div className="w-full md:w-1/3">
            <img 
              src="https://images.ray-ban.com/is/image/RayBan/805289126577__002.png?impolicy=RB_Product&width=1024" 
              alt="Ray-Ban Wayfarer" 
              className="w-full h-auto object-contain"
            />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-bold mb-2">Ray-Ban Wayfarer Classic (RB2140)</h2>
            <p className="text-slate-500 text-sm mb-4">Monitorando o preço oficial no site da Ray-Ban Brasil.</p>
            <div className="flex items-center gap-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-400 mb-1">Alerta abaixo de:</label>
                <div className="flex items-center">
                  <span className="text-2xl font-bold text-green-600">R$</span>
                  <input 
                    type="number" 
                    value={threshold} 
                    onChange={(e) => setThreshold(e.target.value)}
                    className="text-2xl font-bold text-green-600 bg-transparent border-none w-24 focus:ring-0"
                  />
                </div>
              </div>
              <div className="h-10 w-[1px] bg-slate-200"></div>
              <a href={productUrl} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:underline">
                Ver no site <ExternalLink size={14} />
              </a>
            </div>
          </div>
        </div>

        {/* Tabs Content */}
        {activeTab === 'setup' ? (
          <div className="space-y-6">
            <section className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <Github size={20} /> Como configurar de graça
              </h3>
              <div className="space-y-4 text-slate-600">
                <div className="flex gap-4">
                  <div className="bg-slate-100 text-slate-800 font-bold h-8 w-8 rounded-full flex items-center justify-center shrink-0">1</div>
                  <div>
                    <p className="font-bold text-slate-800">Crie um repositório no GitHub</p>
                    <p className="text-sm">Dê o nome de <code>rayban-price-tracker</code> e deixe-o como privado.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="bg-slate-100 text-slate-800 font-bold h-8 w-8 rounded-full flex items-center justify-center shrink-0">2</div>
                  <div>
                    <p className="font-bold text-slate-800">Crie o seu Bot de Notificação</p>
                    <p className="text-sm">A forma mais fácil é pelo <b>Telegram</b>: Fale com o <code>@BotFather</code>, crie um bot e pegue o TOKEN.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="bg-slate-100 text-slate-800 font-bold h-8 w-8 rounded-full flex items-center justify-center shrink-0">3</div>
                  <div>
                    <p className="font-bold text-slate-800">Configure as Secrets no GitHub</p>
                    <p className="text-sm">Vá em Settings {'>'} Secrets and Variables {'>'} Actions e adicione:</p>
                    <ul className="list-disc ml-5 text-xs mt-2 font-mono bg-slate-50 p-2 rounded">
                      <li>TELEGRAM_TOKEN: (token do seu bot)</li>
                      <li>TELEGRAM_CHAT_ID: (seu id de usuário)</li>
                    </ul>
                  </div>
                </div>
              </div>
            </section>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl flex gap-3">
                <AlertCircle className="text-blue-500 shrink-0" />
                <p className="text-xs text-blue-800">O GitHub Actions permite rodar esse script a cada hora ou dia sem cobrar nada.</p>
              </div>
              <div className="bg-green-50 border border-green-100 p-4 rounded-xl flex gap-3">
                <Send className="text-green-500 shrink-0" />
                <p className="text-xs text-green-800">O bot do Telegram enviará a mensagem direto no seu celular instantaneamente.</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-slate-900 rounded-xl p-4 overflow-x-auto">
              <div className="flex justify-between items-center mb-4 border-b border-slate-700 pb-2">
                <span className="text-slate-400 text-xs font-mono">tracker.py</span>
                <button className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded hover:bg-slate-700">Copiar</button>
              </div>
              <pre className="text-blue-300 text-sm font-mono leading-relaxed">
{`import requests
from bs4 import BeautifulSoup
import os

# Configurações
URL = "${productUrl}"
PRECO_ALVO = ${threshold}
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Busca o preço (a classe pode mudar, é ideal verificar no site)
    # Geralmente a Ray-ban usa meta tags de schema.org
    price_tag = soup.find("meta", property="product:price:amount")
    
    if price_tag:
        price = float(price_tag["content"])
        print(f"Preço atual: R$ {price}")
        
        if price <= PRECO_ALVO:
            send_notification(price)
    else:
        print("Preço não encontrado. Verifique se o seletor mudou.")

def send_notification(price):
    msg = f"🚨 PROMOÇÃO RAY-BAN!\\n\\nO Wayfarer Classic está por R$ {price}!\\n\\nLink: {URL}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(send_url)

if __name__ == "__main__":
    check_price()`}
              </pre>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-6">
              <h3 className="font-bold mb-2 flex items-center gap-2"><Code size={18} /> Fluxo do GitHub Actions</h3>
              <p className="text-xs text-slate-500 mb-4">Crie um arquivo em <code>.github/workflows/main.yml</code>:</p>
              <pre className="bg-slate-50 p-3 rounded text-[10px] font-mono border border-slate-100">
{`name: Price Monitor
on:
  schedule:
    - cron: '0 * * * *' # Roda a cada hora
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests beautifulsoup4
      - name: Run script
        env:
          TELEGRAM_TOKEN: \${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: \${{ secrets.TELEGRAM_CHAT_ID }}
        run: python tracker.py`}
              </pre>
            </div>
          </div>
        )}
      </main>

      <footer className="max-w-4xl mx-auto p-6 text-center text-slate-400 text-xs">
        Desenvolvido para uso pessoal • Sem custos de servidor
      </footer>
    </div>
  );
};

export default App;
