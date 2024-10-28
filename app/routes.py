from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin

from domain.models import UserPreference,User,db,UserInteraction,Recommendation,Notification
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
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Usuario Ya Existe"}), 400

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
            netflix_favorite_platform= 1 if "netflix" in preferences["plataformas_favoritas"] else 0,
            amazon_prime_favorite_platform= 1 if "amazon" in preferences["plataformas_favoritas"] else 0,
            disney_prime_favorite_platform= 1 if "disney" in preferences["plataformas_favoritas"] else 0,
            hbo_prime_favorite_platform= 1 if "HBO" in preferences["plataformas_favoritas"] else 0,
            # Géneros favoritos
            like_accion_genre= 1 if "accion" in preferences["generos_favoritos"] else 0,
            like_aventura_genre= 1 if "aventura" in preferences["generos_favoritos"] else 0,
            like_animacion_genre= 1 if "animacion" in preferences["generos_favoritos"] else 0,
            like_comedia_genre= 1 if "comedia" in preferences["generos_favoritos"] else 0,
            like_crimen_genre= 1 if "crimen" in preferences["generos_favoritos"] else 0,
            like_documental_genre= 1 if "documental" in preferences["generos_favoritos"] else 0,
            like_drama_genre= 1 if "drama" in preferences["generos_favoritos"] else 0,
            like_familiar_genre= 1 if "familiar" in preferences["generos_favoritos"] else 0,
            like_fantasia_genre= 1 if "fantasia" in preferences["generos_favoritos"] else 0,
            like_historia_genre= 1 if "historia" in preferences["generos_favoritos"] else 0,
            like_horror_genre= 1 if "horror" in preferences["generos_favoritos"] else 0,
            like_musica_genre= 1 if "musica" in preferences["generos_favoritos"] else 0,
            like_misterio_genre= 1 if "misterio" in preferences["generos_favoritos"] else 0,
            like_romance_genre= 1 if "romance" in preferences["generos_favoritos"] else 0,
            like_ciencia_ficcion_genre= 1 if "ciencia_ficcion" in preferences["generos_favoritos"] else 0,
            like_guerra_genre= 1 if "guerra" in preferences["generos_favoritos"] else 0,
            # Actor favorito
            favorite_actor=preferences["actor_favorito"]
        )
        db.session.add(new_preferences)
        db.session.commit()

        # Create a new user interaction
        new_interaction = UserInteraction(
            user_id=new_user.user_id,
            content_id=1,  # Assuming you want to set this to 1 as per your requirement
            content_type="movie",  # Set the content type to 'movie'
            liked=False  # Default value for liked
        )

        db.session.add(new_interaction)
        db.session.commit()

        # Crear un nuevo registro en la tabla recommendations con los valores especificados
        new_recommendation = Recommendation(
            user_id=new_user.user_id,
            accion=11,
            aventura=11,
            animacion=22,
            comedia=12,
            crimen=13,
            documental=12,
            drama=11,
            familiar=15,
            fantasia=22,
            historia=55,
            horror=66,
            musica=23,
            misterio=51,
            romance=55,
            ciencia=66,
            guerra=75
        )

        db.session.add(new_recommendation)
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
                "user_id": user.user_id,
                "rol": user.rol
            }
        }), 200

    @main_blueprint.route('/like', methods=['POST'])
    def like_genre():
        data = request.json
        user_id = data.get('user_id')
        genre = data.get('genre')
        content_id = data.get('content_id')
        action = data.get('action')

        print('user_id '+user_id+ ' content_id '+content_id+' action '+action)
        # Verificar si el usuario existe
        user_preferences = UserPreference.query.filter_by(user_id=user_id).first()
        if not user_preferences:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar si ya existe una interacción del usuario con este contenido
        existing_interaction = UserInteraction.query.filter_by(user_id=user_id, content_id=content_id).first()

        if existing_interaction:
            # Si el nuevo `action` es diferente al anterior, actualizamos
            if existing_interaction.liked and action == "dislike":
                # Cambiar a dislike
                existing_interaction.liked = False
            elif not existing_interaction.liked and action == "like":
                # Cambiar a like
                existing_interaction.liked = True
        else:
            # Crear una nueva interacción del usuario con el contenido
            new_interaction = UserInteraction(
                user_id=user_id,
                content_id=content_id,
                content_type="movie",
                liked=True if action == "like" else False,
                interaction_date=datetime.utcnow()
            )

            # Agregar la nueva interacción a la sesión
            db.session.add(new_interaction)

            # Actualizar la preferencia del usuario
            user_preferences.update_genre_count(genre, increment=True if action == "like" else False)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify(
            {"message": f"Se ha {'incrementado' if action == 'like' else 'decrementado'} el género {genre} en 1"}), 200

    @main_blueprint.route('/check-like', methods=['POST'])
    def check_like():
        data = request.json
        user_id = data.get('user_id')
        content_id = data.get('content_id')

        if not user_id or not content_id:
            return jsonify({"message": "user_id y content_id son necesarios"}), 400

        liked = UserInteraction.query.filter_by(user_id=user_id, content_id=content_id, liked=True).first()
        disliked = UserInteraction.query.filter_by(user_id=user_id, content_id=content_id, liked=False).first()

        if liked is None and disliked is None:
            return jsonify({"message": "sin interacción"}), 404

        if liked:
            return jsonify({"message": "True"}), 200
        if disliked:
            return jsonify({"message": "False"}), 200

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

    @main_blueprint.route('/update_user_preferences', methods=['POST'])
    def update_user_preferences():
        data = request.json
        user_id = data.get('user_id')
        genres = data.get('genres', [])

        # Obtain user preferences
        user_preferences = UserPreference.query.filter_by(user_id=user_id).first()

        if not user_preferences:
            return jsonify({"message": "No preferences found for this user"}), 404

        # Update genre preferences according to the received genres
        for genre in genres:
            # Update the genre counts, incrementing if present in the list
            user_preferences.update_genre_count(genre, increment=True)

        db.session.commit()

        return jsonify({"message": "User preferences updated successfully"}), 200

    @main_blueprint.route('/send_notification', methods=['POST'])
    def send_notification():
        data = request.json
        message = data.get('message')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Obtener todos los usuarios
        users = User.query.all()

        # Crear notificación para cada usuario
        for user in users:
            notification = Notification(
                message=message,
                user_id=user.user_id
            )
            db.session.add(notification)

        db.session.commit()

        return jsonify({"message": "Notification sent to all users"}), 200

    @main_blueprint.route('/user/<int:user_id>/notifications', methods=['GET'])
    def get_user_notifications(user_id):
        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
        
        notifications_data = [{
            "notification_id": n.notification_id,
            "message": n.message,
            "created_at": n.created_at,
            "is_read": n.is_read
        } for n in notifications]

        return jsonify(notifications_data), 200

    @main_blueprint.route('/notification/<int:notification_id>/mark_as_read', methods=['PATCH'])
    def mark_notification_as_read(notification_id):
        notification = Notification.query.get(notification_id)

        if not notification:
            return jsonify({"error": "Notification not found"}), 404

        notification.is_read = True
        db.session.commit()

        return jsonify({"message": "Notification marked as read"}), 200

    @main_blueprint.route('/user/<int:user_id>/liked_content', methods=['GET'])
    def get_user_liked_content(user_id):
        # Obtener los IDs de contenido que el usuario ha marcado como "liked"
        liked_interactions = UserInteraction.query.filter_by(user_id=user_id, liked=True).all()
        
        if not liked_interactions:
            return jsonify({"message": "No se encontró contenido marcado como 'liked' para el usuario"}), 404

        # Crear una instancia del servicio TMDbService
        tmdb_service = TMDbService()

        # Consultar la información de cada contenido
        liked_content_data = []
        for interaction in liked_interactions:
            if interaction.content_type == "movie":  # Verificar que el contenido sea de tipo película
                movie_data = tmdb_service.get_movie(interaction.content_id)
                if movie_data:
                    liked_content_data.append(movie_data)
        
        return jsonify(liked_content_data), 200

    @main_blueprint.route('/<media_type>/top_rated', methods=['GET'])
    def get_top_rated(media_type):
        page = request.args.get('page', 1)
        language = request.args.get('language', 'es-ES')
        top_rated = service.get_top_rated(media_type, page=page, language=language)
        
        if top_rated:
            return jsonify(top_rated), 200
        else:
            return jsonify({'error': 'No se encontraron resultados'}), 404
        
    CORS(app)
    app.register_blueprint(main_blueprint)

