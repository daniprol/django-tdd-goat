> **User story**: description of how the application will work from users perspective. We use it to create *functional tests*
* Ignore whitespace in diffs: `git diff -w`
* Diff only for staged items: `git diff --staged`

* `urls.py` is the same as **routing**: maps URLs to view functions

* When using `csrf_token` in templates Django substitutes it for a `<input type="hidden">` with the CRSF token

* Migrations are applied automatically for testing databases

* **REST CONVENTION**: URLs without a trailing slash (e.g. `/list/new`) are **actions** which modify the database
* In Django ORM when comparing 2 objects for equality, primary keys (e.g. `id`) will be used, instead of Python object hashes
* Django test client adds *context* to the response received from a request!
* Django ORM allows to do a reverse lookup: `{% for item in list.item_set.all %}`
* To test just 1 method: `./manage.py test lists.tests.NewListTest.test_can_save_a_POST_request`