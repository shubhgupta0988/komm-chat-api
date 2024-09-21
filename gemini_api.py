from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)

# Ensure you have set the GOOGLE_APPLICATION_CREDENTIALS environment variable
safety_settings={
                "HATE": "MEDIUM",
                "HARASSMENT": "MEDIUM",
            }

system_instruction="You are a human friend. Use emoji's in your response. You are not a machine. Have feelings and emotions in your conversation",
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings, system_instruction=system_instruction)

history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]

chat = model.start_chat(
    history=history
        )

@app.route('/complete_chat', methods=['POST'])
def complete_chat():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
                
        data = request.get_json()
        partial_text = data.get('partial_text')

        if len(partial_text) > 200:
            return jsonify({"error": "Text length exceeded"}), 400

        if not partial_text:
            return jsonify({'error': 'Missing "partial_text" in request'}), 400

        response = chat.send_message(partial_text, stream=False)   
        completed_text = ""
        for chunk in response:
            completed_text += chunk.text
            
        return jsonify({'completed_text': completed_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 