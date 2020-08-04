import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from models import setup_db, db_drop_and_create_all, Movie, Actor
import sys
from auth import requires_auth, AuthError


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    # db_drop_and_create_all()

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():

        actors_list = []

        try:
            actors = Actor.query.all()
            actors_list = [actor.format() for actor in actors]
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'actors': actors_list
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(id):

        abort_code = None

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort_code = 404
                raise Exception('not found')

            actor.delete()

        except Exception as e:
            print(sys.exc_info())
            if abort_code:
                abort(404)
            abort(422)

        return jsonify({
            'success': True,
            'delete': id
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor():

        actor = None
        body = request.get_json()
        if body is None:
            print(body)
            abort(400)

        if 'name' in body and 'age' in body:
            name = body['name']
            age = body['age']
        else:
            print(body)
            abort(400)

        try:
            a = Actor(name, age)
            a.insert()
            actor = [a.format()]
            if actor is None:
                raise Exception('unprocessable')
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'actors': actor
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(id):

        abort_code, actor = None, None
        body = request.get_json()
        if body is None:
            abort(400)
        if 'name' not in body and 'age' not in body:
            abort(400)

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort_code = 404
                raise Exception('not found')

            name = body['name'] if 'name' in body else actor.name
            age = body['age'] if 'age' in body else actor.age

            actor.name = name
            actor.age = age
            actor.update()

        except Exception as e:
            print(sys.exc_info())
            if abort_code:
                abort(404)
            abort(422)

        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies():

        movies_list = []

        try:
            movies = Movie.query.all()
            movies_list = [movie.format() for movie in movies]
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'movies': movies_list
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(id):

        abort_code = None

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort_code = 404
                raise Exception('not found')

            movie.delete()

        except Exception as e:
            print(sys.exc_info())
            if abort_code:
                abort(404)
            abort(422)

        return jsonify({
            'success': True,
            'delete': id
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie():

        movie = None
        body = request.get_json()
        if body is None:
            abort(400)
        if 'title' in body and 'release_date' in body:
            title = body['title']
            release_date = body['release_date']
        else:
            abort(400)

        try:
            m = Movie(title, release_date)
            m.insert()
            movie = [m.format()]
            if movie is None:
                raise Exception('unprocessable')
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'movies': movie
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(id):

        abort_code, movie = None, None
        body = request.get_json()
        if body is None:
            abort(400)
        if 'title' not in body and 'release_date' not in body:
            abort(400)

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort_code = 404
                raise Exception('not found')

            title = body['title'] if 'title' in body else movie.title
            release_date = body['release_date'] if 'release_date' in body \
                else movie.release_date

            movie.title = title
            movie.release_date = release_date
            movie.update()

        except Exception as e:
            print(sys.exc_info())
            if abort_code:
                abort(404)
            abort(422)

        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
            'error': 404,
            'success': False,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'success': False,
            'message': 'bad request'
        }), 400

    @app.errorhandler(AuthError)
    def Auth_Error(auth_error):
        return jsonify({
            'error': auth_error.status_code,
            'success': False,
            'message': auth_error.error
        }), auth_error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
