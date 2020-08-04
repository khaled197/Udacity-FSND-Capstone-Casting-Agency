import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie, Actor


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://postgres:postgres@{}/{}" \
            .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        #
        self.actor = {
            "name": "Anne Hathaway",
            "age": 35
        }

        self.another_actor = {
            "name": 'Tom Hanks'
        }

        self.movie = {
            "title": "Inception",
            "release_date": "2010-4-20"
        }
        self.another_movie = {
            "title": "the terminal",
        }
        self.assistant_token = \
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CV' +\
            'UE2X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0a' +\
            'DAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1Nzc2NDExNzk1NjkwNj' +\
            'E0OTczIiwiYXVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF' +\
            '1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY1MzAxODgsImV4cCI6MTU5' +\
            'NjUzNzM4OCwiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOb' +\
            'lciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbn' +\
            'MiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.IZA7Vt9gKMFC-tmlgjG' +\
            'LjjGqISXXo2AcOvGztwbJhinZNaociyZJzD52yQc3P1DGXPT4STlXkyNs3WCM' +\
            'bHXmQ-1oe7HrQJjMm-3FN6OB9tU62RFDhn5q1l4nJWMuDR2FMER6ETQFdoXef' +\
            'mQB95D6uvNGoYsGkcm9nB4e_gA-1Hn-5w-by74QTuIZEy180WoWP4WKg821aD' +\
            'FpHDwpV_0Tq80cys5gA_3nQboYAwXDfMZbzl8q1Yts9BMydkkt-09S9H9o-nr' +\
            'Tf09MW3qR7j6BgpJCBbRongyDB4Ni4v8FcHCKASwEzTvXnh1EQzTsD7yVnw2q' +\
            '9wZjzs6__QKFSeRXmw'

        self.director_token = \
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5C' + \
            'VUE2X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0' +\
            'aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA5NDgwNzI4MTYxNDg5M' +\
            'DExNjc5IiwiYXVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLm' +\
            'F1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY1MzAxMjUsImV4cCI6MTU' +\
            '5NjUzNzMyNSwiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlO' +\
            'blciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvb' +\
            'nMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIi' +\
            'wicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0' +\
            '.BCvrR8bsGn_EIo2TlEpWHzy4OrxSiA02HGOTqgqWNtzya-KyXg5XQHaIgvZ8' +\
            'drP8Wjyn3ifZRKc0R8vgFAtCXfBuX5pNCU4bw_BMADOtT05HXbnipaql6ox3Z' +\
            'OBw8jOcDQb3K-yFWlYr2piLu0_Aa6r_x6AMum8x_HT7KcoN0n63v269mUHwuE' +\
            'pAxj3JlF7GMHs3do3FwDz8lWV2ZZouD7uOwek1VnHHlReUz0_W3r9blAzewH2' +\
            'qlifGr2Iud8DDiBxxX7cVctOJJ7fAmv1mbIpDzOV7nsnZTnTpn--_M-BD-ODo' +\
            'dO2Kc7HAUOX-qv56s1cREnLITU0qxS3MNPLziA'

        self.executive_token = \
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CV' +\
            'UE2X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0a' +\
            'DAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1NDIxMTk3Nzc4NTY3NT' +\
            'g5NzA2IiwiYXVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF' +\
            '1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY1Mjk5NjIsImV4cCI6MTU5' +\
            'NjUzNzE2MiwiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOb' +\
            'lciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbn' +\
            'MiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3J' +\
            'zIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIs' +\
            'InBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.fXsg1inlEVehqoYb1i2Mj' +\
            'aRyLUjv6bzjZT-4ePI-F81a3d3ybdHHxS9o-YgfroyN-E9Tj6OiWP8yV3FOIO' +\
            'DVBTbBHsWw2MWY1P8VE2qPmyxDfwPU3bWvTcdjGfuaycTNELoNhVYg-kY56D2' +\
            'torPM0JX2BQUjDb9tGi3ErngVJ-GLlqnQpRG9wY05wIxXrcR7BiACfXKa2N5H' +\
            'Jih8N2w5gdsaB4ms_KAcvlMmysJKpMbkoF6I3p7mHOx8ZPr95weGHRLlX5BWo' +\
            'Sax351cY9J36zcnsIJEKDrc0Fn41qeCPxoiQniE7ci0l9hrQ0Ve5sMzWTh_J1' +\
            'pIOZQuCkSKPdikXg'

        self.assistant_header = {
            "Authorization": "Bearer {}".format(self.assistant_token)}

        self.director_header = {
            "Authorization": "Bearer {}".format(self.director_token)}

        self.producer_header = {
            "Authorization": "Bearer {}".format(self.executive_token)}

        # add some movies and actors objects to the database for testing
        for i in range(0, 10):
            res = self.client().post('/actors', json=self.actor,
                                     headers=self.producer_header)
            res2 = self.client().post('/movies', json=self.movie,
                                      headers=self.producer_header)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests for casting assistant

    def test_assistant_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)
        # print(self.assistant_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_assistant_401_post_actors(self):
        res = self.client().post('/actors', json=self.actor,
                                 headers=self.assistant_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_assistant_401_patch_actors(self):
        res = self.client().patch('actors/1', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_401_delete_actor(self):
        res = self.client().delete('actors/1', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['movies'], list)

    def test_assistant_401_post_movies(self):
        res = self.client().post('/movies', json=self.movie,
                                 headers=self.assistant_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_assistant_401_patch_movies(self):
        res = self.client().patch('movies/1', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_401_delete_movies(self):
        res = self.client().delete('movies/1', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # tests for Casting Director

    def test_director_get_actors(self):
        res = self.client().get('/actors', headers=self.director_header)
        data = json.loads(res.data)
        # print(self.director_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_director_post_actors(self):
        res = self.client().post('/actors', json=self.actor,
                                 headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_director_400_post_actors(self):
        res = self.client().post('/actors', json=self.another_actor,
                                 headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_director_patch_actors(self):
        res = self.client().patch('actors/1', json={'age': 50},
                                  headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_director_400_patch_actors(self):
        res = self.client().patch('actors/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_director_delete_actors(self):
        res = self.client().delete('actors/2', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_404_delete_actors(self):
        res = self.client().delete('actors/100', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_director_get_movies(self):
        res = self.client().get('/movies', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['movies'], list)

    def test_director_401_post_movies(self):
        res = self.client().post('/movies', json=self.movie,
                                 headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_director_400_patch_movies(self):
        res = self.client().patch('movies/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_director_401_delete_movies(self):
        res = self.client().delete('movies/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # Tests for Executive producer_header

    def test_producer_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_header)
        data = json.loads(res.data)
        # print(self.producer_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_producer_post_actors(self):
        res = self.client().post('/actors', json=self.actor,
                                 headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_producer_400_post_actors(self):
        res = self.client().post('/actors', json=self.another_actor,
                                 headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_producer_patch_actors(self):
        res = self.client().patch('actors/3', json={'age': 50},
                                  headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['actors'], list)

    def test_producer_400_patch_actors(self):
        res = self.client().patch('actors/1', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_producer_delete_actors(self):
        res = self.client().delete('actors/4', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_404_delete_actors(self):
        res = self.client().delete('actors/100', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_producer_get_movies(self):
        res = self.client().get('/movies', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['movies'], list)

    def test_producer_post_movies(self):
        res = self.client().post('/movies', json=self.movie,
                                 headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['movies'], list)

    def test_producer_400_post_movies(self):
        res = self.client().post('/movies', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_producer_patch_movies(self):
        res = self.client().patch('movies/1', json={'title': 'Django'},
                                  headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['movies'], list)

    def test_producer_400_patch_movies(self):
        res = self.client().patch('movies/2', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_producer_delete_movies(self):
        res = self.client().delete('movies/2', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_producer_404_delete_movies(self):
        res = self.client().delete('movies/100', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
