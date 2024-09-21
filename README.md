# Chat API with Google Generative AI

This project implements a RESTful API that generates conversational responses based on user input using Google Generative AI. It features a user interface built with Gradio for easy interaction and a suite of tests to ensure reliability.

## Overview

- **app.py**: The main API application that handles incoming chat requests and returns generated responses.
- **myui.py**: A user interface for the API using Gradio, allowing users to interact with the chat functionality.
- **test_app.py**: Unit tests for the API to ensure all endpoints work as expected and to handle edge cases.

## Features

- Chat completion using Google Generative AI.
- User-friendly UI for testing the API.
- Robust error handling and response validation.
- Comprehensive unit tests for reliability.

## Installation

### Prerequisites

- Python 3.x
- pip

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/shubhgupta0988/komm-chat-api.git
   cd komm-chat-api

2. Create a .env file in the root of the project directory and add your Google API key:

   GOOGLE_GEMINI_API=<Key>

3. Install the required packages:
    
   pip install -r requirements.txt

Usage

Running the API
To start the API server, run:
    python app.py

Running the UI
In a separate terminal, run:
    python myui.py

This will launch a Gradio interface where you can interact with the chat API.

API Endpoint
POST /complete_chat
Request
Content-Type: application/json

Body:
{
    "partial_text": "Your question here"
}

Response
Status: 200 OK
Content:
{
    "completed_text": "Generated response from the AI."
}

Testing
To run the tests, execute:

pytest test_app.py

This will run all the unit tests defined in test_app.py.

Error Handling
The API includes error handling for various scenarios:

Missing partial_text in the request body.
Non-JSON requests.
Blocked prompts due to safety concerns.
Unexpected server errors.
Contributing
Contributions are welcome! Please create an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.