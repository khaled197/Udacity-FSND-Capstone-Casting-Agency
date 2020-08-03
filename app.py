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


AUTH0_DOMAIN = 'fsnd-night.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'login'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():

    auth_headers, auth_parts = None, None

    if 'Authorization' in request.headers:
        auth_headers = request.headers['Authorization']
    if auth_headers:
        auth_parts = auth_headers.split(' ')
    if auth_parts is not None and len(auth_parts) == 2 and \
            auth_parts[0].lower() == 'bearer':

        return auth_parts[1]

    else:
        raise AuthError({'code': 'invalid header',
                        'description': 'Authorization header is malformed'},
                        401)


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
    !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in
    the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({'code': 'invalid claim',
                        'description': 'permissions not included in jwt'}, 401)

    if permission not in payload['permissions']:
        raise AuthError({'code': 'unauthorized',
                        'description': 'permission not found'}, 401)

    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
        https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': (
                                'Incorrect claims. Please, check the audience'
                                ' and issuer.'
                                )
            }, 401)
        except Exception:
            print(sys.exc_info())
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims
        and check the requested permission
    return the decorator which passes the decoded payload
        to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(*args, **kwargs)
            except:
                print(sys.exc_info())

        return wrapper
    return requires_auth_decorator


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    db_drop_and_create_all()

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
        if 'name' in body and 'age' in body:
            name = request.get_json()['name']
            age = request.get_json()['age']
        else:
            abort(400)

        try:
            a = Actor(name, age)
            a.insert()
            actor = [d.format()]
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
        if 'title' in body and 'release_date' in body:
            title = request.get_json()['title']
            release_date = request.get_json()['age']
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


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
