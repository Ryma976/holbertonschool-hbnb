import unittest

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestModels(unittest.TestCase):

    def test_create_user(self):
        user = User("Ali", "Ahmed", "ali@test.com")
        self.assertEqual(user.first_name, "Ali")
        self.assertEqual(user.last_name, "Ahmed")
        self.assertEqual(user.email, "ali@test.com")

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
        self.assertEqual(place.price, 100.0)

    def test_create_amenity(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_create_review(self):
        review = Review(
            "Excellent",
            5,
            "place_id",
            "user_id"
        )
        self.assertEqual(review.text, "Excellent")
        self.assertEqual(review.rating, 5)

    def test_relationships(self):
        place = Place(
            "Villa",
            "Nice",
            200,
            20,
            40,
            "owner"
        )

        amenity = Amenity("Pool")
        review = Review(
            "Great",
            5,
            place.id,
            "user"
        )

        place.add_amenity(amenity.id)
        place.add_review(review)

        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(len(place.reviews), 1)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Ali", "Ahmed", "wrong-email")

    def test_invalid_place_price(self):
        with self.assertRaises(ValueError):
            Place(
                "Villa",
                "Nice",
                -10,
                20,
                40,
                "owner"
            )

    def test_invalid_place_latitude(self):
        with self.assertRaises(ValueError):
            Place(
                "Villa",
                "Nice",
                100,
                100,
                40,
                "owner"
            )

    def test_invalid_place_longitude(self):
        with self.assertRaises(ValueError):
            Place(
                "Villa",
                "Nice",
                100,
                20,
                200,
                "owner"
            )

    def test_invalid_review(self):
        with self.assertRaises(ValueError):
            Review(
                "",
                6,
                "place",
                "user"
            )

    def test_invalid_amenity(self):
        with self.assertRaises(ValueError):
            Amenity("")

    def test_update_model(self):
        user = User("Ali", "Ahmed", "ali@test.com")
        old_updated = user.updated_at

        user.update({
            "first_name": "Omar"
        })

        self.assertEqual(user.first_name, "Omar")
        self.assertNotEqual(old_updated, user.updated_at)


if __name__ == "__main__":
    unittest.main()
