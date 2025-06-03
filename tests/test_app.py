import json
from unittest.mock import patch
from flask.testing import FlaskClient
from app.main import create_app


def test_analyze_route_success():
    app = create_app()
    client: FlaskClient = app.test_client()
    with patch('app.main.build_crew') as mock_build_crew:
        mock_crew = mock_build_crew.return_value
        mock_crew.kickoff.return_value = 'ok'
        response = client.post('/analyze', json={'query': 'SELECT * FROM table'})
        assert response.status_code == 200
        assert response.json == {'result': 'ok'}
        mock_build_crew.assert_called_once()
        mock_crew.kickoff.assert_called_once()


def test_analyze_route_missing_query():
    app = create_app()
    client: FlaskClient = app.test_client()
    response = client.post('/analyze', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'query is required'}

