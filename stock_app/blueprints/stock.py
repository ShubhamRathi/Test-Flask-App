from flask import Blueprint, render_template
import requests
from pprint import pprint

stock = Blueprint('stock', __name__)


def fetch_price(ticker):
    data = requests.get('https://financialmodelingprep.com/api/v3/stock/real-time-price/{}'.format(ticker.upper()),
                        params={'apikey': 'demo'}).json()
    return data["price"]


def fetch_income(ticker):
    try:
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}'.format(
            ticker)
        req = requests.get(url, params={
            'period': 'quarter', 'apikey': 'demo'})
        financials = req.json()["financials"]
        financials.sort(key=lambda quarter: quarter["date"])
        pprint(financials)
        return financials
    except KeyError as err:
        raise KeyError("Key error from fetch_income")


@stock.route('/<string:ticker>')
def view_stock(ticker):
    stock_price = fetch_price(ticker)
    return render_template('stock/stock_quote.html', ticker=ticker, stock_price=stock_price)


@stock.route('/<string:ticker>/financials')
def financials(ticker):
    try:
        financials = fetch_income(ticker)
        chart_data = [float(q["EPS"]) for q in financials if q["EPS"]]
        chart_params = {"type": 'line',
                        "data": {
                            'labels': [q["date"] for q in financials if q["EPS"]],
                            'datasets': [{'label': 'EPS', 'data': chart_data}]
                        }}
        return render_template('stock/financials.html', ticker=ticker, financials=financials, chart_params=chart_params)
    except KeyError:
        raise


@stock.route('/<string:ticker>/simple_financials')
def simple_financials(ticker):
    financials = fetch_income(ticker)
    return render_template('stock/financials_without_chart.html', ticker=ticker, financials=financials)


@stock.route('/<string:ticker>/fake_financials')
def fake_financials(ticker):
    fake_financials = [
        {
            "date": "Q1 20",
            "Revenue": "$120M",
            "Gross Margin": "0.01",
            "EPS": 1.20,
        },
    ]
    return render_template('stock/financials_without_chart.html', ticker=ticker, financials=fake_financials)
