from flask import Flask

from .routes import configure_routes
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from domain.models import db
from domain.services import IAService

ia_service = None

def create_app():
    global ia_service

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:grado122@localhost/grado'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ia_service = IAService()

    CORS(app)
    print('init')
    configure_routes(app)
    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
        app.run(debug=True)

    return app
