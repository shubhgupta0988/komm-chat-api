from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

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

        data = request.json
        partial_text = data.get('partial_text')

        if not partial_text:
            return jsonify({"error": "Missing 'partial_text' in request body"}), 400

        if len(partial_text) > 200:
            return jsonify({"error": "Text length exceeded"}), 400

        response = chat.send_message(partial_text, stream=False)   
        completed_text = ""
        for chunk in response:
            completed_text += chunk.text

        if completed_text != "":
            return jsonify({"completed_text": completed_text})
        else:
            return jsonify({"error": "Failed to generate a response"}), 500

    except genai.types.generation_types.BlockedPromptException as e:
        return jsonify({"error": "The input was blocked due to safety concerns"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)