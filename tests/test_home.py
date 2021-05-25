from flask import url_for

def test_lookup_redirect(client):
    response = client.post(url_for('home.lookup'), data={'ticker': "NTAP"})
    assert response.status_code == 302
    assert response.location == url_for('stock.view_stock', ticker='NTAP', _external=True)

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Stock App' in response.data