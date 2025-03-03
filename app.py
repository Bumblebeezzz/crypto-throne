from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random
import time
import os

app = Flask(__name__)

# Liste des cryptos à surveiller
CRYPTO_PAIRS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT']

# Données de base pour la simulation
BASE_PRICES = {
    'BTC/USDT': 65000,
    'ETH/USDT': 3500,
    'SOL/USDT': 120,
    'XRP/USDT': 0.55
}

def get_simulated_price(symbol):
    base_price = BASE_PRICES[symbol]
    # Simuler une variation de prix de ±5%
    variation = random.uniform(-0.05, 0.05)
    current_price = base_price * (1 + variation)
    
    return {
        'price': round(current_price, 2),
        'change': round(variation * 100, 2),
        'volume': round(random.uniform(1000000, 10000000), 2),
        'high': round(current_price * (1 + random.uniform(0, 0.02)), 2),
        'low': round(current_price * (1 - random.uniform(0, 0.02)), 2),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }

@app.route('/')
def index():
    return render_template('index.html', 
                         exchanges=['binance', 'kucoin', 'kraken', 'htx'],
                         pairs=CRYPTO_PAIRS)

@app.route('/api/prices')
def get_prices():
    exchange_id = request.args.get('exchange', 'binance')
    data = {}
    for pair in CRYPTO_PAIRS:
        data[pair] = get_simulated_price(pair)
    return jsonify(data)

@app.route('/api/compare')
def compare_prices():
    pair = request.args.get('pair', 'BTC/USDT')
    data = {}
    for exchange in ['binance', 'kucoin', 'kraken', 'htx']:
        # Ajouter une légère variation pour chaque exchange
        price_data = get_simulated_price(pair)
        price_data['price'] *= (1 + random.uniform(-0.01, 0.01))  # ±1% de variation entre exchanges
        data[exchange] = price_data
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8742))
    app.run(host='0.0.0.0', port=port)