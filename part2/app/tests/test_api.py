import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_swagger_docs(self):
        """التأكد من أن مستندات Swagger تعمل"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """اختبار إنشاء مستخدم جديد بنجاح"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testsetup@example.com"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()