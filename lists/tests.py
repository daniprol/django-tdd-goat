from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from .models import Item
from .views import home_page


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        # HttpRequest is the object Django creates when a user makes a request in the browser
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        # Response is in bytes
        html: str = response.content.decode("utf8")
        self.assertIn("<title>To-Do lists</title>", html)
        # self.assertTrue(html.startswith("<html>"))
        self.assertTrue(html.endswith("</html>"))

    def test_home_page_returns_correct_html_2(self):
        response = self.client.get("/")
        # NOTE: "assertContains" tests against the "response.content"
        self.assertContains(response, "<title>To-Do lists</title>")
        # self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")
        # NOTE: assertTemplateUsed only works for responses from test client
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        item_text = "A new list item"
        response = self.client.post("/", data={"item_text": item_text})
        self.assertContains(response, item_text)
        self.assertTemplateUsed(response, "home.html")


class ItemModelTests(TestCase):
    def test_saving_and_retrieving_items(self):
        # NOTE: this wouldn't be a unit test (but a integration one) because it uses a dependency (the db)
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.save()

        saved_items = Item.objects.all()  # returns a Queryset (list-like object)
        # TODO: check that using len() would be more inefficient
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "The second item")
