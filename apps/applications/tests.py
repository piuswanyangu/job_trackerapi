from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.applications.models import ApplicationAnalytics, JobApplication


User = get_user_model()


class JobApplicationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPass123!",
            first_name="Owner",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            first_name="Other",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user_can_manage_only_their_applications(self):
        JobApplication.objects.create(
            user=self.other_user,
            company_name="Hidden Company",
            job_title="Backend Engineer",
            status="applied",
        )

        list_url = reverse("job-application-list")
        create_response = self.client.post(
            list_url,
            {
                "company_name": "Acme",
                "job_title": "Frontend Engineer",
                "status": "applied",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["company_name"], "Acme")
        self.assertEqual(create_response.data["user"], self.user.id)
        self.assertNotEqual(create_response.data["user"], self.other_user.id)

        list_response = self.client.get(list_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["company_name"], "Acme")

        detail_url = reverse("job-application-detail", args=[create_response.data["id"]])
        patch_response = self.client.patch(detail_url, {"status": "interview"}, format="json")

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["status"], "interview")

        delete_response = self.client.delete(detail_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobApplication.objects.filter(id=create_response.data["id"]).exists())

    def test_analytics_counts_applications_by_status(self):
        JobApplication.objects.bulk_create(
            [
                JobApplication(user=self.user, company_name="Acme", job_title="Frontend Engineer", status="applied"),
                JobApplication(user=self.user, company_name="Globex", job_title="API Engineer", status="interview"),
                JobApplication(user=self.user, company_name="Initech", job_title="Platform Engineer", status="offer"),
                JobApplication(user=self.user, company_name="Umbrella", job_title="QA Engineer", status="rejected"),
                JobApplication(user=self.other_user, company_name="Hidden", job_title="Designer", status="offer"),
            ]
        )
        ApplicationAnalytics.objects.update_or_create(
            user=self.user,
            defaults={
                "total_applications": 4,
                "applied": 1,
                "interviewed": 1,
                "offer": 1,
                "rejected": 1,
            },
        )

        response = self.client.get(reverse("analytics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_applications"], 4)
        self.assertEqual(response.data["applied"], 1)
        self.assertEqual(response.data["interviewed"], 1)
        self.assertEqual(response.data["offer"], 1)
        self.assertEqual(response.data["rejected"], 1)
