from flask import Flask
from flask_restful import Api
from .config import Config
from .models import db
from .routes import routes
from .api import UploadAPI


def create_app():
    app = Flask(__name__, static_folder=None, template_folder="../templates")
    # remember to adjust the template_folder dir
    app.config.from_object(Config)

    # Validate configuration
    Config.validate()

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register routes
    app.register_blueprint(routes)

    # Initialize Flask-RESTful API
    api = Api(app)
    api.add_resource(UploadAPI, "/api/upload")

    return app
