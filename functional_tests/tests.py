import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# TODO: slow waiting locally and larger number for CI/CD
MAX_WAIT_SECONDS = 5
SLEEP_INTERVAL = 0.5


# NOTE: NoSuchElementException and StaleElementException errors are often a sign that you need an explicit wait.
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        """Runs before every test method!"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Will close browser even when test fails
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        input_box.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        # FIXME: remove explicit wait
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_multiple_urls(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, "/lists/.+")  # +: one or more

        # Delete cookies to simulate a new user session
        self.browser.delete_all_cookies()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # New user adds an item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")

        new_user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, "/lists/.+")  # +: one or more
        self.assertNotEqual(user_list_url, new_user_list_url)

        # Check there is no trace of the old user list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                # self.assertTrue(
                #     any(row.text == "1: Buy peacock feathers" for row in rows),
                #     f"New todo did not appear in table. Contents were:\n{table.text}",
                # )
                return

            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT_SECONDS:
                    raise
                time.sleep(SLEEP_INTERVAL)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)

        # User browser window is set to specific size
        self.browser.set_window_size(1024, 768)

        # Input should be centered
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + input_box.size["width"] / 2, 512, delta=10)

        # Check that inputbox remains centerd after entering a new item
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(input_box.location["x"] + input_box.size["width"] / 2, 512, delta=10)
