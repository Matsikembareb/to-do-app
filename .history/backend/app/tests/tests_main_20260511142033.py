import json

class TestMain():
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.json == {'message': 'Hello, World!'}

    def test_cors_preflight_allows_local_frontend(self, client):
        response = client.open(
            '/api/auth/login',
            method='OPTIONS',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
            },
        )

        assert response.status_code in (200, 204)
        assert response.headers.get('Access-Control-Allow-Origin') == 'http://localhost:3000'
