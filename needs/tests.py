from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser
from .models import Need

client = APIClient()


class NeedsListTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        self.another_user = CustomUser.objects.create(email="test2@test.com", first_name="ccc", last_name="ddd")

        # create needs
        self.user_need = Need.objects.create(user=self.user, text="bag", contact="0919999999", is_handled=False)
        self.another_user_need = Need.objects.create(user=self.another_user, text="bag", contact="0919999999", is_handled=False)

    def test_get_all_needs(self):
        # test not authenticated user
        response = client.get(reverse("needs"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("needs"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_need(self):
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # test invalid request data
        response = client.post(reverse("needs"), {
            "text": "bag",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test valid request data
        response = client.post(reverse("needs"), {
            "text": "bag",
            "contact": "09190770744"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_need(self):
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # test another user need
        response = client.delete(reverse("need", kwargs={'pk': self.another_user_need.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test user need
        response = client.delete(reverse("need", kwargs={'pk': self.user_need.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)