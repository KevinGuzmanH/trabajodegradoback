from flask import Blueprint, jsonify, request
from domain.services import MovieService

def configure_routes(app):
    main_blueprint = Blueprint('main', __name__)

    @main_blueprint.route('/movie/<string:title>', methods=['GET'])
    def get_movie_info(title):
        service = MovieService()
        movie_info, status_code = service.get_movie_info(title)
        return jsonify(movie_info), status_code

    app.register_blueprint(main_blueprint)
