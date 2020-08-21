from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser
from .models import Event, Cost
import datetime

client = APIClient()


class EventsListTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        # create test events
        self.event_1 = Event.objects.create(name='کوه نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121')
        self.event_1.save()
        self.event_2 = Event.objects.create(name='دره‌ی نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121')
        self.event_2.save()
        self.event_3 = Event.objects.create(name='جنگل نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121')
        self.event_3.save()

    def test_get_all_events(self):
        # test not authenticated user
        response = client.get(reverse("events"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("properties"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_events(self):
        # test not authenticated user
        response = client.get(reverse("events"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated user
        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(reverse("properties/me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventEnrollTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        # create test events
        self.event_1 = Event.objects.create(name='کوه نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        self.event_2 = Event.objects.create(name='دره‌ی نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        self.event_3 = Event.objects.create(name='جنگل نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        # TODO: should .save() be called?

    def test_enroll_event(self):
        # test not authenticated user
        response = client.get(reverse(f"events/{self.event_1.id}"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.login(email="test@test.com", password="12345")
        token = Token.objects.get(user__email="test@test.com")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(reverse(f"events/{self.event_1.id}"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventCostTest(TestCase):
    def setUp(self):
        # create test users
        self.user = CustomUser.objects.create(email="test@test.com", first_name="aaa", last_name="bbb")
        self.user.set_password("12345")
        self.user.save()
        Token.objects.create(user=self.user)

        self.another_user = CustomUser.objects.create(email="test2@test.com", first_name="aaa", last_name="bbb")
        self.another_user.set_password("12345")
        self.another_user.save()
        Token.objects.create(user=self.another_user)

        # create test events
        self.event_1 = Event.objects.create(name='کوه نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        self.event_2 = Event.objects.create(name='دره‌ی نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        self.event_3 = Event.objects.create(name='جنگل نابی', length=4, date=datetime.date(2020, 8, 11), gender='M',
                                            description='غذا', coordination_date=datetime.date(2020, 8, 8),
                                            difficulty_level='طاقت‌فرسا', coordinator='قاسم پشه',
                                            coordinator_phone_number='09122212121').save()
        # create test costs
        self.cost_1 = Cost.objects.create(event=self.event_1, user=self.user, description='کشک', amount=15).save()
        self.cost_2 = Cost.objects.create(event=self.event_1, user=self.another_user, description='لوبیا', amount=30).save()

    def test_event_costs_view(self):
    def test_event_cost_view(self):
    def test_user_event_cost(self):
