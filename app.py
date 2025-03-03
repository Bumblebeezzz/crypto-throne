from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random
import time
import os
import json

app = Flask(__name__)

# Liste des meme coins à surveiller
MEME_COINS = ['DOGE/USD', 'SHIB/USD', 'PEPE/USD', 'FLOKI/USD', 'BONK/USD', 'WIF/USD']

# Données de base pour la simulation
BASE_PRICES = {
    'DOGE/USD': 0.15,
    'SHIB/USD': 0.000025,
    'PEPE/USD': 0.0000095,
    'FLOKI/USD': 0.0002,
    'BONK/USD': 0.00003,
    'WIF/USD': 0.25
}

# Historique des prix pour les graphiques
price_history = {coin: [] for coin in MEME_COINS}
max_history_length = 20  # Nombre de points de données à conserver

def get_simulated_price(symbol):
    base_price = BASE_PRICES[symbol]
    # Simuler une variation de prix plus volatile pour les meme coins (±10%)
    variation = random.uniform(-0.10, 0.10)
    current_price = base_price * (1 + variation)
    
    # Ajouter un peu de bruit pour simuler des mouvements de marché réalistes
    market_sentiment = random.uniform(-0.02, 0.02)
    current_price *= (1 + market_sentiment)
    
    # Formater le prix en fonction de sa valeur
    if current_price < 0.001:
        formatted_price = f"{current_price:.8f}"
    elif current_price < 0.01:
        formatted_price = f"{current_price:.6f}"
    elif current_price < 1:
        formatted_price = f"{current_price:.4f}"
    else:
        formatted_price = f"{current_price:.2f}"
    
    price_data = {
        'price': current_price,
        'formatted_price': formatted_price,
        'change': round(variation * 100, 2),
        'volume': round(random.uniform(5000000, 100000000), 2),
        'high': round(current_price * (1 + random.uniform(0, 0.05)), 8),
        'low': round(current_price * (1 - random.uniform(0, 0.05)), 8),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    # Ajouter au historique des prix
    price_history[symbol].append(price_data['price'])
    if len(price_history[symbol]) > max_history_length:
        price_history[symbol].pop(0)
    
    price_data['history'] = price_history[symbol]
    
    return price_data

@app.route('/')
def index():
    return render_template('index.html', 
                         coins=MEME_COINS)

@app.route('/api/prices')
def get_prices():
    data = {}
    for coin in MEME_COINS:
        data[coin] = get_simulated_price(coin)
    return jsonify(data)

@app.route('/api/coin/<coin_symbol>')
def get_coin_detail(coin_symbol):
    if coin_symbol not in MEME_COINS:
        return jsonify({"error": "Coin not found"}), 404
    
    # Simuler des données plus détaillées pour un coin spécifique
    price_data = get_simulated_price(coin_symbol)
    
    # Ajouter des données supplémentaires
    price_data['market_cap'] = round(price_data['price'] * random.uniform(1000000000, 10000000000), 2)
    price_data['supply'] = round(random.uniform(100000000000, 1000000000000), 0)
    price_data['rank'] = random.randint(30, 100)
    
    return jsonify(price_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8742))
    app.run(host='0.0.0.0', port=port)