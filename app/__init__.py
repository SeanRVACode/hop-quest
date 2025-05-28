from flask import Flask
from app.routes import main_bp
from flask_bootstrap import Bootstrap5


def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    # Configure app
    app.register_blueprint(main_bp)

    # Register blue prints
    return app
