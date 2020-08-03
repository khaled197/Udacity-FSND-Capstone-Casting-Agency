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
            '1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY0ODM0MzAsImV4cCI6MTU5' +\
            'NjQ5MDYzMCwiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOb' +\
            'lciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbn' +\
            'MiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.npdokXQkmbpyHvn1Egf' +\
            'tIi3tdWuLAwHHmNDUhvbYkbL5gYeW1Xdks5dBwDk3Uba3w6-1RtauLvXbE_Xe' +\
            'yemyOd0onaRqYVx8Vr6QN94DP4m6zkQO7ga7DKw_LvtL1_k0Lx5aNKo25hRiH' +\
            'R8Q4Oo6hCf6BeBmD7aZ7HiK_OkLHLAgXAlXIwNVx_wXUgvwGK4A27VxszyoJ9' +\
            'ON2w5zLTeKpAGamyLewb25G6U1cWUgwa75VDKjqY0spIfNikhbiNDbnRKrXv2' +\
            '4UWmIfIC3CpWhrzzWk8L7AVSipdsjIkTBYRIvvFVbESomT_y_HpWxVqXxfVlF' +\
            'Xli_JiMfvyuDiQOvrw'

        self.director_token = \
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CV' +\
            'UE2X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0a' +\
            'DAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA5NDgwNzI4MTYxNDg5MD' +\
            'ExNjc5IiwiYXVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF' +\
            '1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY0ODMzMTUsImV4cCI6MTU5' +\
            'NjQ5MDUxNSwiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOb' +\
            'lciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbn' +\
            'MiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiw' +\
            'icGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.' +\
            'nWFqBXreCWtn_8cZ5-CkiZSztXVJMNhdbFR_fSu0id55-IuEhTfkhuDk9XNh_' +\
            'UFaKFM7KYF2CK779jZ-ADVvLdWwxuutmrHriTQGiwMvQhGah0HmL2fT1yjmPY' +\
            'VBVOSF5DEFX1Gbd_48xSdocqb3exw8T7fPDAvQQf_eAzyQuXN_RhOgxymR_0z' +\
            '11fn6ZCGvnXfUSaVGBOvWCDj03arAz4Z2I_CnjhSFHbbthTzsev2L8F18ajgm' +\
            '7mB_h-zB8NwcXUEFOKO9kFYQ6gedJOrkiyTqn-0gtYSVPYPBiZn4xi24LuBd0' +\
            '2MaKsE6f8yjVu6LZZNRxod4qj-ivUCnRdS16w'

        self.executive_token = \
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CV' +\
            'UE2X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0aD' +\
            'AuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1NDIxMTk3Nzc4NTY3NTg5' +\
            'NzA2IiwiYXVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF1dG' +\
            'gwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTY0ODMwMzMsImV4cCI6MTU5NjQ5' +\
            'MDIzMywiYXpwIjoiY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOblciLC' +\
            'JzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsi' +\
            'ZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2' +\
            'V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6' +\
            'YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.je-WNsVNNvZDKdDVuw3VFnFHdlvDmi' +\
            '_TdkykCpL9w6MYawFFb-BdZ5WEQXu1cyMnaDGIiOQrF1cJz_hzJT4M-xAfH6Ve' +\
            'BKLiKEV4XKeI-L1Ro6Q48z3al9cxUT2t1M_AfreCujAezcIgfHpdBiTkfkdLSK' +\
            'X2kdodZtw4Me9Ytveb9X8FPpxYJCaLiFNWZe09VKHC7Du58t49Aj7IYU6jevzG' +\
            'fhEvPaGC6aQQ5Tzc_m_OZZA7y-jSNr656UMpjFIdvk5z6PBfNoOV_nw0VA4Mro' +\
            'iGR0r59-A5nRJ6LFu_G6mCzacNTMQvqfEyBhntYXI1KnI82mdxSra1PmO2Peclpg'

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
