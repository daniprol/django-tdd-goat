from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from .models import Item, List
from .views import home_page

# NOTE: each TestCase method uses a transaction that will be rolled back => clean database state between tests

# setUp: runs for each test.
# setUpTestData (classmethod): runs once. Useful to reuse data for all methods


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


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        mylist = List.objects.create()
        Item.objects.create(text="item1", list=mylist)
        Item.objects.create(text="item2", list=mylist)
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "item1")
        self.assertContains(response, "item2")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        item_text = "A new list item"
        response = self.client.post("/lists/new", data={"item_text": item_text})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

        # self.assertContains(response, item_text)
        # self.assertTemplateUsed(response, "home.html")

        # self.assertRedirects(response, "/")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # NOTE: this wouldn't be a unit test (but a integration one) because it uses a dependency (the db)
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.list = mylist
        second_item.save()

        # get() will error ir 0 or >1 results are found
        saved_list = List.objects.get()
        # NOTE: they will be compared by "id" primary key and not hash
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()  # returns a Queryset (list-like object)
        # TODO: check that using len() would be more inefficient
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "The second item")
        self.assertEqual(second_saved_item.list, mylist)
