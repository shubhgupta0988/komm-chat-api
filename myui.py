import gradio as gr

import requests
import json

def complete_chat(partial_text):
  """
  Invokes the REST API to complete a chat message.

  Args:
    partial_text: The partial text of the chat message.

  Returns:
    The completed text from the API response.
  """

  url = "http://localhost:5000/complete_chat"
  headers = {"Content-Type": "application/json"}
  data = {"partial_text": partial_text}

  response = requests.post(url, headers=headers, data=json.dumps(data))

  if response.status_code == 200:
    try:
      response_json = response.json()
      return response_json.get("completed_text")
    except json.JSONDecodeError:
      print("Error decoding JSON response.")
      return None
  else:
    print(f"Error: API request failed with status code {response.status_code}")
    return None

def generate_response(message, chat_history):
    #bot_message = f"Testing ... {message}"
    bot_message = complete_chat(message)
    chat_history.append((message, bot_message))
    return "", chat_history


with gr.Blocks() as demo:
  chatbot = gr.Chatbot()
  message = gr.Textbox(placeholder="Enter your message here...")
  clear = gr.Button("Clear")

  message.submit(generate_response, [message, chatbot], [message, chatbot])
  clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(share=False, debug=True)
