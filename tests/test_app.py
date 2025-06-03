import os
import sys
from unittest.mock import patch
from flask.testing import FlaskClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import create_app


def test_index_get():
    app = create_app()
    client: FlaskClient = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form' in response.data


def test_index_post_success():
    app = create_app()
    client: FlaskClient = app.test_client()
    with patch('app.main.build_crew') as mock_build_crew:
        mock_crew = mock_build_crew.return_value
        mock_crew.kickoff.return_value = 'ok'
        response = client.post('/', data={'query': 'SELECT * FROM table'})
        assert response.status_code == 200
        assert b'ok' in response.data
        mock_build_crew.assert_called_once()
        mock_crew.kickoff.assert_called_once()


def test_index_post_missing_query():
    app = create_app()
    client: FlaskClient = app.test_client()
    response = client.post('/', data={'query': ''})
    assert response.status_code == 200
    assert b'query is required' in response.data
