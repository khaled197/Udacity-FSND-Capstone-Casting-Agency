import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


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

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
        #
        self.actor = {
            "name": "Anne Hathaway",
            "age": 35
        }

        self.another_actor = {
            "name": 'Tom Hanks'
        }

        self.movie = {
            "title": "Saving private ryan",
            "release_date": "2004-4-20"
        }
        self.another_movie = {
            "title": "the terminal",
        }

        self.assistant_header = {
            "Authorization": "Bearer " +
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CVUE2 \
            X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0aDAuY29t \
            LyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1Nzc2NDExNzk1NjkwNjE0OTczIiwiY \
            XVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF1dGgwLmNvbS91c2 \
            VyaW5mbyJdLCJpYXQiOjE1OTY0NTc5NzUsImV4cCI6MTU5NjQ2NTE3NSwiYXpwIjo \
            iY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOblciLCJzY29wZSI6Im9wZW5p \
            ZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdld \
            Dptb3ZpZXMiXX0.tTnzAgogh6_tpWwdYIh-stFBc7mz8Kln_mBTDs4JLYdqBCUl8P \
            3pD56PiCL5Ak4qcwvihHDJiBwehL1hNO2ZN3ETTkl92-bE_WB3i-NQ9KqEdrHERQ5 \
            13bGhg32wu9ZgRIgg-Etn_KxiM5eHFE_RmrtDktWA36bAhSlA2FFR_NdbwCgR0oLO \
            pkmtr7BpIiBVau49IZ1YEo-1HVjqY8jh-C3ZXHkbE764_O_Nyy3OmJ754gjO5Tpe9 \
            vu1QCf4MF92pmR1ifFeEx68FgLlVXv71-wXIM7DPDOzZpyaT9G_VsMxTvSzEZ-mG1 \
            SzAhSUPCL0fBhfbgZReUrLLz7u-T8oCw"
        }

        self.producer_header = {
            "Authorization": "Bearer " +
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CVUE2 \
            X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0aDAuY29t \
            LyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1NDIxMTk3Nzc4NTY3NTg5NzA2IiwiY \
            XVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF1dGgwLmNvbS91c2 \
            VyaW5mbyJdLCJpYXQiOjE1OTY0NTgzNTYsImV4cCI6MTU5NjQ2NTU1NiwiYXpwIjo \
            iY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOblciLCJzY29wZSI6Im9wZW5p \
            ZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsI \
            mRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOm \
            FjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXM \
            iXX0.Zl9wo-SlbqDmWpZEeEpZa9c78UvQC9_gvTnMabE9G5YYVZHhOCOP6ElSZopb \
            ZNda9IvDuXhen_SmeWLsee1USgKphM8W8wuTMyLUjL6zSa2D6jw6cO3oZWIuQhuQ0 \
            xT1XjCbjaK7yPcnWRPh4eHASqoqdOreaoiqSyiFOCGywSKIo_hVN4oY98lBixERnH \
            9fiaSS_Kas_sPu72_YptW4ncd2f-9O7F4ofo4xIwozDtdpoG67ZPQw2aQmWG5OwcF \
            _LqB2Lreo_Rg5ZwpUGgD6FpoY-TF8ScM6Pct-tO2GyMUkLoxIW0t285lLrpps2F2s \
            o-Qcu2ZZ8Ern2SWEKBAMHg"
        }
        self.director_header = {
            "Authorization": "Bearer " +
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJvQmJ2LTFCSE5CVUE2 \
            X3dRdDZJbCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmlnaHQudXMuYXV0aDAuY29t \
            LyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA5NDgwNzI4MTYxNDg5MDExNjc5IiwiY \
            XVkIjpbImxvZ2luIiwiaHR0cHM6Ly9mc25kLW5pZ2h0LnVzLmF1dGgwLmNvbS91c2 \
            VyaW5mbyJdLCJpYXQiOjE1OTY0NTgxNTgsImV4cCI6MTU5NjQ2NTM1OCwiYXpwIjo \
            iY3ZkWjFOQkZISmVmZVJOSEl0emIxZ0ZQdlRkMHlOblciLCJzY29wZSI6Im9wZW5p \
            ZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsI \
            mdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW \
            92aWVzIiwicG9zdDphY3RvcnMiXX0.RIndDxjDrge0zJOOGeVFKN6UIEkkm69QCOd \
            IEghY7LFxMV2U7j5HOoZCjzAAccG8p7hLMs7VOlug_0p6a3h7UEOny7eV5uGE-6Bf \
            LAwRE3kLV7egPFlF9GRMyX6NH45zN5pj0i1_CePT6B6xxlrneobEJN-gi3OpBafZx \
            YBcGJrwdbEpa4whXT0lL2zLqkSM137tpVjXi27cRxMsYrgWCpiDyZGad-e4CnDYvw \
            MM7O7qWJacd99-CQGztsigWlDol6nr4NLyZSWNzfaKElsehytzJd8BSKDxWETlgXS \
            7DnZ96rRlQhsRjecZiAgoKhMUh82s3-Y2XyzJvwdOw7tcZQ"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests for casting assistant

    def test_assistant_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)

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
        res = self.client().delete('actors/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['delete'], integer)

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
        res = self.client().patch('actors/1', json={'age': 50},
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
        res = self.client().delete('actors/1', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['delete'], integer)

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
        res = self.client().patch('movies/1', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_producer_delete_movies(self):
        res = self.client().delete('movies/1', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_producer_404_delete_movies(self):
        res = self.client().delete('movies/100', headers=self.producer_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)















# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
