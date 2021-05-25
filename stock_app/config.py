import os


class BaseConfig:
    STOCK_API_BASE_URL = "https://financialmodelingprep.com/api/v3/"
    STOCK_API_KEY = os.getenv(
        'STOCK_API_KEY', '30042f14ea4fb3f4685674db648bfdc3')


class DevConfig(BaseConfig):
    EXPLAIN_TEMPLATE_LOADING = True
    ENV = 'development'


class ProdConfig(BaseConfig):
    ENV = 'production'


class TestConfig(BaseConfig):
    ENV = 'test'


configurations = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}
