from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@127.0.0.1/blogly-test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for views for Pets."""

    #Make a user to test database

    # def setUp(self):
    #     """Add sample pet."""

    #     Pet.query.delete()

    #     pet = Pet(name="TestPet", species="dog", hunger=10)
    #     db.session.add(pet)
    #     db.session.commit()

    #     self.pet_id = pet.id

    # def tearDown(self):
    #     """Clean up any fouled transaction."""

    #     db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            #assert user on page
            self.assertIn('TestPet', html)