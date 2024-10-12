from flask import Blueprint, jsonify, request

from domain.models import UserPreference,User,db
from domain.services import TMDbService
import json

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
            return content, 200
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
        db.session.commit()
        # Procesar las preferencias del usuario
        preferences = {
            "frecuencia_visualizacion": data.get('frecuenciavisualizacion'),
            "generos_favoritos": data.get('generofavorito', []),
            "plataformas_favoritas": data.get('plataformasfavoritas', []),
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

    @app.route('/recommendations/<int:user_id>', methods=['GET'])
    def recommend(user_id):
        # Verificamos si el servicio de IA está disponible
        from app import ia_service

        # Verificamos si el servicio de IA está disponible
        if ia_service is None:
            return jsonify({"error": "IA service not initialized"}), 500

        # Obtener las recomendaciones para el usuario
        recommendations = ia_service.get_recommendations_for_user(user_id)

        # Example: [[3, 11, 12, 22, 13, 12, 11, 15, 22, 55, 66, 23, 51, 55, 66, 75]]
        # Ignore the first item (user_id), and work with the rest of the array
        if not recommendations or len(recommendations) == 0:
            return jsonify({"error": "No recommendations found"}), 404

        # Define the genres in their respective order
        genre_list = [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Adventure"},
            {"id": 16, "name": "Animation"},
            {"id": 35, "name": "Comedy"},
            {"id": 80, "name": "Crime"},
            {"id": 99, "name": "Documentary"},
            {"id": 18, "name": "Drama"},
            {"id": 10751, "name": "Family"},
            {"id": 14, "name": "Fantasy"},
            {"id": 36, "name": "History"},
            {"id": 27, "name": "Horror"},
            {"id": 10402, "name": "Music"},
            {"id": 9648, "name": "Mystery"},
            {"id": 10749, "name": "Romance"},
            {"id": 878, "name": "Science Fiction"},
            {"id": 10752, "name": "War"}
        ]
        # Extract user recommendations (ignoring the first element, which is user_id)
        user_recommendations = recommendations[0][1:]

        # Create a new dictionary with "id" and corresponding rec numbers
        id_rec_dict = {genre["id"]: user_recommendations[i] for i, genre in enumerate(genre_list)}

        # Get the top 5 IDs with their corresponding values, sorted by values in descending order
        top_5_ids = sorted(id_rec_dict.items(), key=lambda item: item[1], reverse=True)[:5]

        # Extract just the IDs from the sorted list
        top_5_ids_only = [id for id, value in top_5_ids]

        # Prepare a list to hold content recommendations
        content_recommendations = []

        # Map the top genre IDs to their respective genre information
        for genre_id in top_5_ids_only:
            # Ensure the genre_id is valid
            genre_info = next((genre for genre in genre_list if genre["id"] == genre_id), None)

            if genre_info is not None:
                content = get_content_by_genre(genre_info['id'])

                content_recommendations.append({
                    "genre_name": genre_info['name'],
                    "content": content
                })


        return jsonify(content_recommendations)

    app.register_blueprint(main_blueprint)

