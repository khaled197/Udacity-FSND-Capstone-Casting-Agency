import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie, Actor

ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')


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

        self.assistant_header = {
            "Authorization": "Bearer {}".format(ASSISTANT_TOKEN)}

        self.director_header = {
            "Authorization": "Bearer {}".format(DIRECTOR_TOKEN)}

        self.producer_header = {
            "Authorization": "Bearer {}".format(PRODUCER_TOKEN)}

        # add some movies and actors objects to the database for testing
        # for i in range(0, 10):
        #     res = self.client().post('/actors', json=self.actor,
        #                              headers=self.producer_header)
        #     res2 = self.client().post('/movies', json=self.movie,
        #                               headers=self.producer_header)

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
