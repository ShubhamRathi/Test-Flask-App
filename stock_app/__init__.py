from flask import Flask, render_template

from stock_app.blueprints.home import home as home_bp
from stock_app.blueprints.stock import stock as stock_bp
from stock_app.config import DevConfig, ProdConfig, configurations


# def create_app(environment_name='dev'):
#     app = Flask(__name__)
#     app.config.from_object(configurations[environment_name])

#     if environment_name == "dev":
#         app.config.from_object(DevConfig)
#     else:
#         app.config.from_object(ProdConfig)
#         @app.errorhandler(500)
#         def handle_error(execption):
#             return render_template('500.html'), 500
    
#     app.register_blueprint(home_bp)
#     app.register_blueprint(stock_bp, url_prefix='/stocks')

#     return app

def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    app.register_blueprint(home_bp)
    app.register_blueprint(stock_bp)

    @app.errorhandler(500)
    def handle_error(exception):
        return render_template('500.html'), 500  # pragma: no cover

    return app