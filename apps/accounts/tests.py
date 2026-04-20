from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsApiTests(APITestCase):
    def test_user_can_register_login_and_read_profile(self):
        register_payload = {
            "email": "candidate@example.com",
            "first_name": "Jane",
            "last_name": "Candidate",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        register_response = self.client.post(reverse("register"), register_payload, format="json")

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(register_response.data["email"], register_payload["email"])
        self.assertNotIn("password", register_response.data)

        login_response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": register_payload["email"], "password": register_payload["password"]},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        profile_response = self.client.get(reverse("me"))

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["email"], register_payload["email"])
        self.assertEqual(profile_response.data["first_name"], register_payload["first_name"])
