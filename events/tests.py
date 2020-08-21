from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser, UserProfile
from .models import Event
import datetime

client = APIClient()


class EventsListTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

    def test_get_all_events(self):
        # test not authenticated user
        response = client.get(reverse("events"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("events"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_events(self):
        # test not authenticated user
        response = client.get(reverse("user_events"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("user_events"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventEnrollTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        # create test events
        self.event = Event.objects.create(name='کوه نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121')

    def test_enroll_event(self):
        # test not authenticated user
        response = client.post(reverse("event_enroll", kwargs={"pk": self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # test no profile user
        response = client.post(reverse("event_enroll", kwargs={"pk": self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        # test with profile user but not matched gender
        user_profile = UserProfile.objects.get(user=self.user.id)
        user_profile.gender = 'F'
        user_profile.is_completed = True
        user_profile.save()
        response = client.post(reverse("event_enroll", kwargs={"pk": self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        # test with profile user with matcher gender
        user_profile.gender = 'M'
        user_profile.save()
        response = client.post(reverse("event_enroll", kwargs={"pk": self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test get has_enrolled in event
        response = client.get(reverse("event_enroll", kwargs={"pk": self.event.id}))
        self.assertEqual(response.data, {"has_enrolled": True})