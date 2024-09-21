import pytest
from flask import json
from unittest.mock import patch, MagicMock
import google.generativeai as genai
from google.generativeai.types import StopCandidateException, BlockedPromptException
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_chat_success(client):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        mock_response = MagicMock()
        mock_response.text = "This is a test response."
        mock_generate.return_value = mock_response

        response = client.post('/complete_chat',
                               json={'partial_text': 'Test input'},
                               content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'completed_text' in data
        assert data['completed_text'] == "This is a test response."

def test_complete_chat_missing_partial_text(client):
    response = client.post('/complete_chat',
                           json={},
                           content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Missing 'partial_text' in request body"

def test_complete_chat_non_json_request(client):
    response = client.post('/complete_chat',
                           data='This is not JSON',
                           content_type='text/plain')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Request must be JSON"

def test_complete_chat_blocked_prompt(client):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        mock_generate.side_effect = BlockedPromptException("Blocked prompt")

        response = client.post('/complete_chat',
                               json={'partial_text': 'Blocked input'},
                               content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "The input was blocked due to safety concerns"

def test_complete_chat_generation_exception(client):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        mock_generate.side_effect = StopCandidateException("Generation failed")

        response = client.post('/complete_chat',
                               json={'partial_text': 'Failed input'},
                               content_type='application/json')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert "An unexpected error occurred: Generation failed" in data['error']

def test_complete_chat_unexpected_exception(client):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        mock_generate.side_effect = Exception("Unexpected error")

        response = client.post('/complete_chat',
                               json={'partial_text': 'Error input'},
                               content_type='application/json')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "An unexpected error occurred: Unexpected error"

def test_complete_chat_empty_response(client):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        mock_response = MagicMock()
        mock_response.text = ""
        mock_generate.return_value = mock_response

        response = client.post('/complete_chat',
                               json={'partial_text': 'Empty response'},
                               content_type='application/json')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == "Failed to generate a response"