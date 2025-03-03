from flask import Flask, render_template, jsonify, request
import ccxt
import pandas as pd
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

# Configuration des exchanges
exchanges = {
    'binance': ccxt.binance(),
    'kucoin': ccxt.kucoin(),
    'kraken': ccxt.kraken(),
    'htx': ccxt.htx()
}

# Liste des cryptos à surveiller
CRYPTO_PAIRS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT']

def get_crypto_price(exchange_id, symbol):
    try:
        exchange = exchanges[exchange_id]
        ticker = exchange.fetch_ticker(symbol)
        return {
            'price': ticker['last'],
            'change': ticker['percentage'],
            'volume': ticker['quoteVolume'],
            'high': ticker['high'],
            'low': ticker['low'],
            'timestamp': datetime.fromtimestamp(ticker['timestamp']/1000).strftime('%H:%M:%S')
        }
    except Exception as e:
        print(f"Erreur pour {exchange_id} - {symbol}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html', 
                         exchanges=list(exchanges.keys()),
                         pairs=CRYPTO_PAIRS)

@app.route('/api/prices')
def get_prices():
    exchange_id = request.args.get('exchange', 'binance')
    data = {}
    for pair in CRYPTO_PAIRS:
        price_data = get_crypto_price(exchange_id, pair)
        if price_data:
            data[pair] = price_data
    return jsonify(data)

@app.route('/api/compare')
def compare_prices():
    pair = request.args.get('pair', 'BTC/USDT')
    data = {}
    for exchange_id in exchanges:
        price_data = get_crypto_price(exchange_id, pair)
        if price_data:
            data[exchange_id] = price_data
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8742))
    app.run(host='0.0.0.0', port=port) 