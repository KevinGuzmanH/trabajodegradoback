from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    country = db.Column(db.String(100))

# User Preferences model
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    watch_frequence_by_week = db.Column(db.Integer)
    netflix_favorite_platform = db.Column(db.Boolean)
    amazon_prime_favorite_platform = db.Column(db.Boolean)
    disney_prime_favorite_platform = db.Column(db.Boolean)
    hbo_prime_favorite_platform = db.Column(db.Boolean)
    like_accion_genre = db.Column(db.Boolean)
    like_aventura_genre = db.Column(db.Boolean)
    like_animacion_genre = db.Column(db.Boolean)
    like_comedia_genre = db.Column(db.Boolean)
    like_crimen_genre = db.Column(db.Boolean)
    like_documental_genre = db.Column(db.Boolean)
    like_drama_genre = db.Column(db.Boolean)
    like_familiar_genre = db.Column(db.Boolean)
    like_fantasia_genre = db.Column(db.Boolean)
    like_historia_genre = db.Column(db.Boolean)
    like_horror_genre = db.Column(db.Boolean)
    like_musica_genre = db.Column(db.Boolean)
    like_misterio_genre = db.Column(db.Boolean)
    like_romance_genre = db.Column(db.Boolean)
    like_ciencia_ficcion_genre = db.Column(db.Boolean)
    like_guerra_genre = db.Column(db.Boolean)
    favorite_actor = db.Column(db.String(100))
