from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser
from .models import CustomUser

client = APIClient()


class MyProfileViewTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

    def test_my_profile_view(self):
        # test not authenticated user
        response = client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)