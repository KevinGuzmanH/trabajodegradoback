from flask import Flask
from .routes import configure_routes
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from domain.models import db
from domain.services import IAService
from domain.models import UserPreference, User, UserInteraction, Recommendation, Notification

ia_service = None

def create_app():
    global ia_service

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:grado122@localhost/grado'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ia_service = IAService()

    CORS(app)
    configure_routes(app)

    with app.app_context():
        db.create_all()
        print('Tablas creadas.')
        
        existing_admin = User.query.filter_by(username="admin").first()
        if existing_admin:
            print("El usuario 'admin' ya existe.")
        else:
            # Crear el usuario "admin"
            admin_user = User(
                email="admin@example.com",
                username="admin",
                password="admin_password",  # Cambia esto a una contraseña segura
                age=30,
                gender="none",
                country="Country",
                rol="admin"
            )
            db.session.add(admin_user)
            db.session.commit()

            # Crear las preferencias de usuario para el "admin"
            admin_preferences = UserPreference(
                user_id=admin_user.user_id,
                watch_frequence_by_week=3,
                netflix_favorite_platform=1,
                amazon_prime_favorite_platform=1,
                disney_prime_favorite_platform=1,
                hbo_prime_favorite_platform=0,
                like_accion_genre=1,
                like_comedia_genre=1,
                like_drama_genre=1,
                favorite_actor="Actor Favorito"
            )
            db.session.add(admin_preferences)
            
            # Crear la interacción de usuario para el "admin"
            admin_interaction = UserInteraction(
                user_id=admin_user.user_id,
                content_id=1,
                content_type="movie",
                liked=False
            )
            db.session.add(admin_interaction)

            # Crear recomendaciones para el "admin"
            admin_recommendation = Recommendation(
                user_id=admin_user.user_id,
                accion=10,
                aventura=10,
                animacion=10,
                comedia=10,
                crimen=10,
                documental=10,
                drama=10,
                familiar=10,
                fantasia=10,
                historia=10,
                horror=10,
                musica=10,
                misterio=10,
                romance=10,
                ciencia=10,
                guerra=10
            )
            db.session.add(admin_recommendation)
            
            # Guardar todos los cambios
            db.session.commit()
            print("Usuario 'admin' creado con éxito.")

    app.run(debug=True)
    return app
