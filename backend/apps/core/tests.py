from django.test import Client, TestCase


class TestModelFactory(TestCase):
    """Обобществлённый завод для создания моделей"""
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')


class ErrorPageTests(TestModelFactory):
    """Проверяем страницы с ошибками страниц

    ---------------------------
    -------- НИД ХЭЛП ---------
    ---------------------------

    """

    # def test_403(self):
    #     response = self.client.get('/403')
    #     self.assertEqual(response.status_code, 403)
    #     self.assertTemplateUsed(response, 'core/403.html')

    # def test_403csrf(self):
    #     """Страница с ошибкой 403csrf существует"""
    #     response = self.client.get('/403csrf')
    #     self.assertEqual(response.status_code, 403)
    #     self.assertTemplateUsed(response, 'core/403csrf.html')

    def test_404(self):
        """Страница с ошибкой 404 существует"""
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')

    # def test_500(self):
    #     """Страница с ошибкой 500 существует"""
    #     response = self.client.get('/500')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertTemplateUsed(response, 'core/500.html')
