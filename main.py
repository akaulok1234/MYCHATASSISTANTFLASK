from flask import Flask, render_template, request, jsonify

import requests
import threading
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY=")


app = Flask(__name__)



def generate_openai_response(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        "max_tokens": 4000,
        "temperature": 0.8,
        "model": "gpt-3.5-turbo"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    # Corrected the key to access the assistant's reply
    return result["choices"][0]["message"]["content"]

def get_openai_response_async(user_message):
    threading.Thread(target=generate_openai_response, args=(user_message,)).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    assistant_reply = generate_openai_response(user_message)  # Call the function synchronously
    return jsonify({'response': assistant_reply})

if __name__ == '__main__':
    app.run()
