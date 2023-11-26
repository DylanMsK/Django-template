from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from core.views import ProjectInfo, HealthCheck

User = get_user_model()
Auth_Header_Type = api_settings.AUTH_HEADER_TYPES[0]


class BaseTestCase(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.username = "testuser"
        self.password = "password"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        print(self.user)

        access_token = AccessToken.for_user(self.user)
        HTTP_AUTHORIZATION = f"{Auth_Header_Type} {access_token}"
        self.client.credentials(HTTP_AUTHORIZATION=HTTP_AUTHORIZATION)


class SystemInfoTest(BaseTestCase):
    PATH = "/v1/system/info/"
    VIEW_NAME = "system:info"
    VIEW = ProjectInfo

    def setUp(self):
        return super().setUp()

    def test_reverse(self):
        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_get(self):
        response = self.client.get(reverse(self.VIEW_NAME))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], "django-template")
        self.assertRegex(data["version"], r"\d+\.\d+\.\d+")


class HealthCheckTest(BaseTestCase):
    PATH = "/v1/system/health/"
    VIEW_NAME = "system:health"
    VIEW = HealthCheck

    def setUp(self):
        return super().setUp()

    def test_reverse(self):
        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_get(self):
        response = self.client.get(reverse(self.VIEW_NAME))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
