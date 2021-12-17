from django.test import Client, TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    """Тест about"""
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.guest_client = Client()

    # Проверяем общедоступные страницы about
    def test_about_exists_at_desired_location(self):
        """Страница /about/author/ доступна любому пользователю."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)

    def test_about_exists_at_desired_location(self):
        """Страница /about/contact/ доступна любому пользователю."""
        response = self.guest_client.get(reverse('about:contact'))
        self.assertEqual(response.status_code, 200)
