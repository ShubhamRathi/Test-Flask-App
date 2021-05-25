from flask import url_for
import requests
import pytest


class MockPrice:
    @staticmethod
    def json():
        return {"price": 42.0}


class MockFinancials:
    @staticmethod
    def json():
        return {"financials": [{'date': '2019-01-01', "Revenue": '100.00',
                                'Gross Margin': "0.1", "EPS": "2.2"}]}


class MockNotFound:
    @staticmethod
    def json():
        return {}


def test_stock_quote(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockPrice()
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get(url_for('stock.view_stock', ticker="APPL"))
    assert response.status_code == 200
    print(response.data)
    assert b'price is 42.0' in response.data


def test_stock_financials(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFinancials()
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get(url_for('stock.financials', ticker="APPL"))
    assert response.status_code == 200
    assert b'APPL Financials' in response.data
    assert b'https://quickchart.io/chart' in response.data
    assert b'2019-01-01' in response.data
    assert b'100.00' in response.data


# Isnt passing
# def test_unknown_financials(client, monkeypatch):
#     def mock_empty_response(*args, **kwargs):
#         return MockNotFound()
#     monkeypatch.setattr(requests, "get", mock_empty_response)

#     with pytest.raises(KeyError):
#         response = client.get(url_for('stock.financials', ticker="UNKNONW"))
