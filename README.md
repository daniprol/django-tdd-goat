> **User story**: description of how the application will work from users perspective. We use it to create *functional tests*
* Ignore whitespace in diffs: `git diff -w`
* Diff only for staged items: `git diff --staged`

* `urls.py` is the same as **routing**: maps URLs to view functions

* When using `csrf_token` in templates Django substitutes it for a `<input type="hidden">` with the CRSF token

* Migrations are applied automatically for testing databases
* **REST CONVENTION**: URLs without a trailing slash (e.g. `/list/new`) are **actions** which modify the database