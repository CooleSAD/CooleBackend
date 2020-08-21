from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser
from .models import Property

client = APIClient()


class PropertiesListTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

    def test_get_all_properties(self):
        # test not authenticated user
        response = client.get(reverse("properties"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("properties"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserPropertiesListTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

    def test_get_my_properties(self):
        # test unauthenticated
        response = client.get(reverse(f"properties/{self.user.id}"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.get(reverse(f"needs/{self.user.id}"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReservePropertyTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        # create props
        self.property_one = Property.objects.create(name='کوله‌ی نابی', kind='backpack', state='F', borrower=self.user,
                                                    price=2000)
        self.property_two = Property.objects.create(name='کیسه‌خواب نابی', kind='sleeping_bag', state='R',
                                                    borrower=self.user, price=1000)
        self.property_three = Property.objects.create(name='طناب نابی', kind='rope', state='C', borrower=self.user,
                                                      price=5000)

    def test_reserve_property(self):
        # test unauthenticated
        response = client.get(reverse(f"properties/{self.property_one.id}"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # reserve confirmed
        response = client.post(reverse(f"properties/{self.property_three.id}"))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        # reserve reserved good
        response = client.post(reverse(f"properties/{self.property_two.id}"))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        # reserve free good
        response = client.post(reverse(f"properties/{self.property_one.id}"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
