from django.test import TestCase
from core.models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.is_active)
