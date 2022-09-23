from fastapi import status
from tests import client


def test_health():
    response = client.get('/api/v1/content/health/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'health': 'ok'}
