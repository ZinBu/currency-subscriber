
async def test_health(client):
    response = await client.get('/healthcheck')
    assert response.status_code == 200
