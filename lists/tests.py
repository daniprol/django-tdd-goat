from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from .views import home_page


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        # HttpRequest is the object Django creates when a user makes a request in the browser
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        # Response is in bytes
        html: str = response.content.decode("utf8")
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.startswith("<html>"))
        self.assertTrue(html.endswith("</html>"))
