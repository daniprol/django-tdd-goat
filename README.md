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
* `LiveServerTestCase` doesn't find *static* files automatically: `StaticLiveServerTestCase` does.

* **TRICK**: use `git reset --hard` in general to cleanup dirty files in your workspace.
* To collect static files and ignore django admin files in the venv: `./manage.py collecstatic --ignore "admin"`

> Testing layout features will only be done as a mean to check that static files and styling is loaded correctly
> You may also want tests for JS features that are tricky to implement

* Use `--failfast` in functional tests to avoid waiting.
* Using `export` will make set the variable permanently in that shell.

## Docker 
* By default `runserver` binds the `127.0.0.1` but that IP is not the network adapter that containers expose to the outside world.
* Use `runserver 0.0.0.0:8000` as Docker command instead.
* Instead of `-v` use `type=bind,source=./src/db.sqlite3,target=/src/db.sqlite3` to mount volumes. This helps showing you errors if the target directory doesn't exist.

## Gunicorn
```bash
gunicorn "superlists.wsgi:application" --bind :5000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --access-logfile="-"
```
* Run locally with production configuration:
```bash
DJANGO_DEBUG_FALSE=1 DJANGO_SECRET_KEY="asdf" DJANGO_ALLOWED_HOST="localhost" gunicorn --bind :5000 superlists.wsgi:application --access-logfile "-"
```
**WARNING:** you need to previously run `./manage.py collectstatic` to get all static files to work (`whitenoise` doesnt work automatically when DEBUG is false)

**IMPORTANT:** unlike Django `runserver`, *gUnicorn* will not discover and serve static files automatically.
* Use `whitenoise` as middleware to serve those files when using gUnicorn **IF `DEBUG=TRUE`** (otherwise, it wont work!)
* To server static files in production you need to run `collectstatic` in the Dockerfile
* To handle static files while using gUnicorn in `DEBUG MODE` you can add to `wsgi.py`:
```python
import os

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")


if settings.DEBUG:
    # Add middleware to handle static files when using gUnicorn in DEBUG MODE
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
```