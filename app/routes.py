from flask import Blueprint, jsonify, request

from domain.models import UserPreference,User,db
from domain.services import TMDbService

def configure_routes(app):
    main_blueprint = Blueprint('main', __name__)
    service = TMDbService()

    @main_blueprint.route('/genres/<media_type>', methods=['GET'])
    def get_genres(media_type):
        try:
            genres = service.get_genres(media_type)
            return jsonify(genres), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @main_blueprint.route('/content/<tipo>', methods=['GET'])
    def get_content_by_tipo(tipo):
        content = service.get_content_by_tipo(tipo)
        if content:
            return jsonify(content), 200
        else:
            return jsonify({'error': 'No se encontró contenido'}), 404

    @main_blueprint.route('/now_playing/<media_type>', methods=['GET'])
    def get_now_playing(media_type):
        page = request.args.get('page', 1)
        content = service.get_now_playing(media_type, page)
        if content:
            return jsonify(content), 200
        else:
            return jsonify({'error': 'No se encontró contenido en emisión'}), 404

    @main_blueprint.route('/external_ids/<media_type>/<int:media_id>', methods=['GET'])
    def get_external_id(media_type, media_id):
        external_ids = service.get_external_id(media_type, media_id)
        if external_ids:
            return jsonify(external_ids), 200
        else:
            return jsonify({'error': 'No se encontraron IDs externos'}), 404

    @main_blueprint.route('/recommended/<media_type>/<int:media_id>', methods=['GET'])
    def get_recommended(media_type, media_id):
        page = request.args.get('page', 1)
        recommendations = service.get_recommended(media_type, media_id, page)
        if recommendations:
            return jsonify(recommendations), 200
        else:
            return jsonify({'error': 'No se encontraron recomendaciones'}), 404

    @main_blueprint.route('/videos/<media_type>/<int:media_id>', methods=['GET'])
    def get_youtube_video(media_type, media_id):
        videos = service.get_youtube_video(media_type, media_id)
        if videos:
            return jsonify(videos), 200
        else:
            return jsonify({'error': 'No se encontraron videos'}), 404

    @main_blueprint.route('/trending/<media_type>/week', methods=['GET'])
    def get_trending(media_type):
        page = request.args.get('page', 1)
        language = request.args.get('language', 'en-US')
        trending = service.get_trending(media_type, page, language)
        if trending:
            return jsonify(trending), 200
        else:
            return jsonify({'error': 'No se encontró contenido en tendencias'}), 404

    @main_blueprint.route('/movie/<int:movie_id>', methods=['GET'])
    def get_movie(movie_id):
        movie = service.get_movie(movie_id)
        if movie:
            return jsonify(movie), 200
        else:
            return jsonify({'error': 'No se encontró la película'}), 404

    @main_blueprint.route('/content/genre/<int:genre_id>', methods=['GET'])
    def get_content_by_genre(genre_id):
        page = request.args.get('page', 1)
        content = service.get_content_by_genre(genre_id, page)
        if content:
            return jsonify(content), 200
        else:
            return jsonify({'error': 'No se encontró contenido para este género'}), 404

    @main_blueprint.route('/register', methods=['POST'])
    def register_user():
        data = request.json
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        age = data.get('age')
        gender = data.get('genre')
        country = data.get('country')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Correo ya utilizado"}), 400

        # Create a new User object
        new_user = User(email=email, username=username, password=password,
                        age=age, gender=gender, country=country)

        db.session.add(new_user)
        db.session.commit()  # Save the user first to get the user_id
        # Procesar las preferencias del usuario
        preferences = {
            "frecuencia_visualizacion": data.get('frecuenciavisualizacion'),
            "generos_favoritos": data.get('generofavorito', []),  # Lista de géneros favoritos
            "plataformas_favoritas": data.get('plataformasfavoritas', []),  # Lista de plataformas favoritas
            "actor_favorito": data.get('actorfavorito')
        }

        # Asignar las preferencias según los valores recibidos
        # Usamos True/False para géneros y plataformas
        new_preferences = UserPreference(
            user_id=new_user.user_id,
            watch_frequence_by_week=preferences["frecuencia_visualizacion"],
            # Plataformas favoritas
            netflix_favorite_platform="netflix" in preferences["plataformas_favoritas"],
            amazon_prime_favorite_platform="amazon" in preferences["plataformas_favoritas"],
            disney_prime_favorite_platform="disney" in preferences["plataformas_favoritas"],
            hbo_prime_favorite_platform="HBO" in preferences["plataformas_favoritas"],
            # Géneros favoritos
            like_accion_genre="accion" in preferences["generos_favoritos"],
            like_aventura_genre="aventura" in preferences["generos_favoritos"],
            like_animacion_genre="animacion" in preferences["generos_favoritos"],
            like_comedia_genre="comedia" in preferences["generos_favoritos"],
            like_crimen_genre="crimen" in preferences["generos_favoritos"],
            like_documental_genre="documental" in preferences["generos_favoritos"],
            like_drama_genre="drama" in preferences["generos_favoritos"],
            like_familiar_genre="familiar" in preferences["generos_favoritos"],
            like_fantasia_genre="fantasia" in preferences["generos_favoritos"],
            like_historia_genre="historia" in preferences["generos_favoritos"],
            like_horror_genre="horror" in preferences["generos_favoritos"],
            like_musica_genre="musica" in preferences["generos_favoritos"],
            like_misterio_genre="misterio" in preferences["generos_favoritos"],
            like_romance_genre="romance" in preferences["generos_favoritos"],
            like_ciencia_ficcion_genre="ciencia_ficcion" in preferences["generos_favoritos"],
            like_guerra_genre="guerra" in preferences["generos_favoritos"],
            # Actor favorito
            favorite_actor=preferences["actor_favorito"]
        )
        db.session.add(new_preferences)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    @main_blueprint.route('/login', methods=['POST'])
    def login_user():
        data = request.json
        email_or_username = data.get('username')
        password = data.get('password')

        # Buscar el usuario por email o username
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar si la contraseña es correcta
        if user.password != password:
            return jsonify({"message": "Contraseña incorrecta"}), 401

        return jsonify({
            "message": "Login exitoso",
            "user": {
                "email": user.email,
                "username": user.username,
                "user_id": user.user_id
            }
        }), 200

    app.register_blueprint(main_blueprint)
