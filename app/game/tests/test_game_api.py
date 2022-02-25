from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Round

ROUND_URL = reverse('round-round-list')
# GAMES_URL = reverse('game:game-list')


def create_round(**params):
    """Helper function to reduce boilerplate code when creating rounds"""
    return get_user_model().objects.create_round(**params)


class PublicRoundApiTests(TestCase):
    """Test the publically available round API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(ROUND_URL) # Makes unauthenticated request to our ROUND_URL
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRoundApiTests(TestCase):
    """Test the authorized user rounds API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test_password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_rounds(self):
        """Test retrieving tags"""
        Round.objects.create(user=self.user, name="Vegan")
        Round.objects.create(user=self.user, name="Dessert")

        res = self.client.get(ROUNDS_URL)

        rounds = Round.objects.all().order_by('-number')
        serializer = RoundSerializer(rounds, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        # We will create new user in addition to the user that is
        # created at the setUp just so we can assign tag to that user
        # and then we can compare that that tag was not included in response
        # because it was not the authenticated user
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        Round.objects.create(user=user2)
        round = Round.objects.create(user=self.user)

        res = self.client.get(ROUND_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['number'], round.number)