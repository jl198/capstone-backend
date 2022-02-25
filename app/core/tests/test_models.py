from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        email = 'test@test.com'
        password = 'test_password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email a user signs up with is normalized (lowercase)"""
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, 'test_password')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test_password")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test_super_user@test.com',
            'test_password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)
