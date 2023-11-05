from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import requests

URL = "http://54.210.73.216:5000"
app = Flask(__name__)

def update_streak(user_id: int, url: str):
    endpoint = f'/upgrade/{user_id}'
    full_url = url + endpoint
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        'timestamp': current_timestamp
    }
    try:
        response = requests.post(full_url, json=payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

def dummy_3rd_party_api():
    return True

@app.route('/payment/<int:user_id>', methods=['POST'])
def payment(user_id):
    payment_successful = dummy_3rd_party_api()
    
    if not payment_successful:
        return jsonify({'error': 'Payment was unsuccessful'}), 400

    streak_update_response = update_streak(user_id, URL)
    
    if streak_update_response:
        return jsonify({'msg': 'Payment successfully proccessed'}), 200
    else:
        return jsonify({'error': 'Failed to update streak'}), 500

if __name__ == '__main__':
    app.run(debug=True)


