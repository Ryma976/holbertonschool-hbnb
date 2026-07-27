import unittest

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestModels(unittest.TestCase):

    def test_create_user(self):
        user = User("Ali", "Ahmed", "ali@test.com")
        self.assertEqual(user.first_name, "Ali")

    def test_create_place(self):
        place = Place(
            "Villa",
            "Nice place",
            100,
            24.7,
            46.6,
            "owner_id"
        )
        self.assertEqual(place.title, "Villa")

    def test_create_amenity(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_relationships(self):
        user = User("Ali", "Ahmed", "ali@test.com")
        place = Place(
            "Villa",
            "Nice",
            200,
            20,
            40,
            "owner"
        )

        amenity = Amenity("Pool")

        place.add_amenity(amenity)

        self.assertEqual(len(place.amenities), 1)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Ali", "Ahmed", "wrong-email")


if __name__ == "__main__":
    unittest.main()
