
# Django for Professionals by William Vincent
This is a bunch of messy notes I took on the book while I was building the project. 
Attempting to save here for further reference. 

### Chapter 1: Local Setup, Venv, Command Line, Git, Python
- Django is a scaling ORM (object-relational-mapper) database, meaning we will use almost identical Django code for any one of several possible databases like PostgreSQL, MariaDB, Oracle, MySQL, and SQLite. The Django ORM handles the translation from Python code to SQL configured for each database automatically.
- Used to create Instagram, Spotify, and Dropbox.
- Best practice is to use the same database locally and in production, making Django's built-in sqlite3 database unsuitable for most production-ready apps.
- Django loads apps from top-to-bottom, so generally good practice is adding new apps below built-in apps they rely on like admin, auth, etc.
- Create a new project: 
  ```
  django-admin startproject <projectname>
  ```
- cd into new folder created and run 
  ```
  python manage.py startapp <appname>
  ```
  to create a new app.
- You then need to add the appname to the list of installed apps in the `settings.py` file in the subfolder for your main app.
- Structure: 
  - `__init__.py` just tells python to treat it like a python directory.
  - `settings.py` has the program guts & backend.
  - `asgi.py` and `wsgi.py` don't need to be edited, but dictate how the program interacts with a browser.
  - `urls` allows you to determine route.
  - `manage.py` allows you to make db migrations, run the server, etc.
- It's not advisable to run migrations before configuring a custom user model. If you do so, Django will bind the database to the built-in user model, which is difficult to modify later on in the project.
- In app folder:
  - Admin allows you to register database models so they can be viewed from the admin panel.
  - Models where you dictate those models.
  - Apps you don't need to worry about.
  - Views allows you to create routes on the website.
- Terminal Commands:
  - cd into project; add django.
  ```
  django-admin startproject <projectname>
  ```
  ```
  cd <projectname>
  ```
  ```
  python manage.py startapp myapp
  ```
  - Django will create files but not recognize the new app until added to the `INSTALLED_APPS` config in `settings.py`.
  ```
  python manage.py runserver
  ```
  ```
  python manage.py makemigrations
  ```
  ```
  python manage.py migrate
  ```
  - ALWAYS create a custom user model before you make your initial migration; if you don't, there will be more complicated problems down the line. Steps to add:
    - Create CustomUser model.
    - Update `django_project/settings.py`.
    - Customize `UserCreationForm` and `UserChangeForm`.
    - Add custom user model to `admin.py`.
    - Create a function call for your user model in `settings.py` so it can be referenced identically across your project, e.g., in `settings.py`, `AUTH_USER_MODEL = "accounts.CustomUser"`.
    - In `forms.py`, `class Meta: model=get_user_model`.
  - The password field is implicitly included in all users by default; we need to extend the `AbstractUser` class that Django provides. 
  ```
  python manage.py createsuperuser
  ```
  ```
  python manage.py runserver
  ```
I understand the need for consistency in formatting for VSCode. I'll ensure the formatting for Chapters 2 to 5 matches the style used in Chapter 1, focusing on VSCode compatibility.

---

### Chapter 2: Docker & Dockerization
- Docker packages software into containers with reliable cross-environment performance.
- Best for sharing system-built apps which can replicate software needs on any machine.
- Mainly used for maintaining a simulation of a production environment locally.
- Two files, `Dockerfile` and `docker-compose.yml`, can be shared with confidence.
- A container is similar to a VM but virtualizes only the OS; multiple containers are run by a single kernel.
- **Dockerfile**: DNA which instructs Docker on how to build an image/snapshot of your software.
- **.dockerignore**: Usually a good place to add `.git`, `.venv`, `.gitignore`.
- **docker-compose.yml**: Set docker version, specify services within docker host.
- **Image**: Read-only template describing how to create a docker container.
- **Container**: An instance of the image.
- Terminal Commands:
  ```
  docker build -t myapp ./
  ```
  ```
  docker run myapp
  ```
  ```
  docker-compose up -d
  ```
  ```
  docker-compose logs
  ```
  ```
  docker-compose down
  ```
  ```
  docker ps
  ```

### Chapter 3: PostgreSQL, Production Databases
- PostgreSQL is recommended for production-ready apps. Use the same database in both local and production environments for best practice.
- Django is a scaling ORM database, suitable for several databases like PostgreSQL, MariaDB, Oracle, MySQL, and SQLite.
- Django ORM automatically handles the translation from Python code to SQL.

### Chapter 4: Starting the Bookstore Project
- Set up new Django, docker, configure Postgres for Bookstore

### Chapter 5: Pages App for Homepage; Robust Testing
- **Testing**:
  - Django’s `SimpleTestCase` is used for webpages without a model.
  - Be descriptive in test naming; start each method with `test`.
  - Example Tests:
    - Check HTTP status code:
      ```
      def test_url_exists_at_correct_location(self):
          response = self.client.get("/")
          self.assertEqual(response.status_code, 200)
      ```
    - Check template usage:
      ```
      def test_homepage_template(self):
          response = self.client.get("/")
          self.assertTemplateUsed(response, "home.html")
      ```
    - Check homepage HTML content:
      ```
      def test_homepage_contains_correct_html(self):
          response = self.client.get("/")
          self.assertContains(response, "home page")
      ```
    - Test URL resolution:
      ```
      def test_homepage_url_resolves_homepageview(self):
          view = resolve("/")
          self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
      ```
- Terminal Commands for Testing:
  ```
  docker-compose exec web python manage.py test [dirName]
  ```

### 6. complete user registration using built-in `auth` app
- **User Registration**:
  - Log in and log out are straightforward since Django provides views and URLs, but Sign up has no built-in solution and is more challenging.
  - For this site we used the `AUTH_USER_MODEL` setting to tell Django to use our custom user model, not the default `User` module here. That's why we have to wait to configure before migrating anything
  - When you run the migrate command for the first time you create 6 installed apps in settings.py which power the site:
    - INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    ]
  - The `user.is_authenticated` check can be used by default in an HTML template to dynamically render different components for logged in users. Also `user.email`
  - Variables are marked in an HTML template by using double open-close brackets {{}}
  - you can use in-project urls in templates:<a href="{%url 'login'%}">Log in</a> 
    - this TEMPLATE TAG {%%} takes as its first argument a named URL pattern
  - users and related variables are automatically available in your template through TEMPLATE CONTEXTS, which mean that a template is loaded with corresponding data from views.py file.
  - you can add csrf protection on any submittable form by adding the {% csrf_token %} template tag to the start of the form. This prevents malicious websites from changing the link, or attacking sites/users. Django already has CSRF middleware for all this!
  - form.as_p displays each form field with a paragraph p tag
  - the logout function uses `LogoutView` in source code, and has URL name `logout`, so it can be referred to in a template tag as just logout. You can also set this with LOGOUT_REDIRECT_URL
  - 5 standard steps to create any new Django page; for the specific case of creating a user registration page:
    - create an app-level accounts/urls.py file
    - update the project-level django_project/urls.py to point to the accounts app 
    - add a view called SignupPageView
    - create a signup.html template file
    - update home.html to display the new page
    - Step order almost doesn't matter since all are needed for signup to work
    - Vincent recommends urls -> views -> templates workflow

### 7. Static asset configuration for CSS, JS, images, Bootstrap
  - for local dev, the Django webserver automatically serves static files with minimal configuration required. They can be placed in an app-level directory called `static`
    - however, because most projects reuse static assets across apps, the more common approach is a base-level `static` directory folder with all files
  - Thus when we eventually push our code to both GitHub and Heroku these empty directories will not appear which can cause problems in deployment when collectstatic is run. To avoid this we add an empty file to each empty directory.
  - by default, for local usage, all static files are at `http://127.0.0.1:8000/static/`
  - built-in `staticfiles` app that ships with django in the INSTALLED_APPS ships with a quick helper view whiich serves files locally for development, and automatically searches for a `static` directory within each app
    - or set the value: `STATICFILES_DIRS = [BASE_DIR / "static"]`
  - static assets must be explicitly loaded into templates using {% load static %} e.g. css must be explicitly loaded to be displayed
  - `collectstatic` - In a production environment, it is far more efficient to combine all static files into one location and serve that in a single, larger HTTP request. `collectstatic` does this for us, but requires the `STATIC_ROOT` and `STATICFILES_STORAGE` configuration in `settings.py`
    - When `collectstatic` is run locally, it combines all available static files defined by STATICFILES_DIRS and places them in a directory defined as `STATIC_ROOT`. For this project, we set `STATIC_ROOT` to be the base directory with the name staticfiles.
    - `STATICFILES_STORAGE` is the file storage engine used. By default, implicitly set to `django.contrib.staticfiles.storage.StaticFilesStorage`, but we make that explicit for this project.
    - finally, run the terminal command `python manage.py collectstatic` to execute
  - BOOTSTRAP can be installed locally or used via a CDN, recommended. Much better to deliver a cached version of Bootstrap's compiled CSS and JS to our project.
  - "For production, the collectstatic command must be run to compile all static files into a single directory specified by STATIC_ROOT. The consolidated files can then be served either on the same server, a separate server, or a dedicated cloud service/CDN by updating STATICFILES_STORAGE."

### 8. Advanced user reg; email-only login & social auth via `django-allauth` 3party package
  - many users use the popular django-allauth third-party package when setting up authentication to prevent security leaks/errors in development
    - install third-party dependency workflow: 
      - add to `requirements.txt`, spin down the current docker container, rebuild the image, and start a new container.
      - update `INSTALLED_APPS` config within `settings.py`
      - configure any additional implicitly set variables in `settings.py`
      - migrate to account for any changes in `settings.py`
    - django-allauth requires an update to Django's `AUTHENTICATION_BACKENDS`. By default, Django includes `ModelBackend` which is needed to login by username in the Django admin. `django-allauth` needs its own additional backend, `AuthenticationBackend`, so users can login by e-mail.
    - you can also reset the implicitly set configuration `EMAIL_BACKEND`, which looks for a cnfiigured SMTP server to send emails by default. `django-allauth` will send such an email on successful registration, but we need to congifure an SMTP server first.
    - Django’s auth app looks for templates within a templates/registration directory, but allauth prefers they be located within a templates/account directory.
    - update the URL links within `templates/_base.html` to use `django-allauth`’s URL names rather than Django’s. We do this by adding an `account_` prefix so Django’s `logout` will now be `account_logout`, `login` will be `account_login`, and `signup` will be `account_signup`.
    - `allauth` also provides a convenient "remember me" box for login creds, which needs to be added in `settings.py` as `ACCOUNT_SESSION_REMEMBER = True`
    - four more config options to set:
      - ACCOUNT_USERNAME_REQUIRED = False
      - ACCOUNT_AUTHENTICATION_METHOD = "email"
      - ACCOUNT_EMAIL_REQUIRED = True
      - ACCOUNT_UNIQUE_EMAIL = True
      - This will require users to create accounts using email, but then auto generate usernames for them based on their email. If you fully remove the username from the custom user model, it requires AbstractBaseUser and is much mre complex.
      - In the case where two usernames with different emails coincide, `django-allauth` automatically adds a random two-digit string to the username.

### 9. environment variables
  - loaded at run time rather than hard coded into database
  - See Twelve-factor App Design; also Django best practice for security and simpler local/production config
  - store any truly secret info apart from the code base, so it's not committed by accident
  - environs package has Django-specific package installs `environs[django]==9.5.0`
  - SECRET_KEY is a randomly generated string used for cryptographic signing and created whenever the startproject command is run.
  - 2 steps to switch environment vars:
    - add environment variable to `docker-compose.yml`
    - update `django_project/settings.py` to point to the var
  - Note that if your `SECRET_KEY` includes a dollar sign, $, then you need to add an additional dollar sign, $$, when copying to docker. This is due to how `docker-compose` handles variable substitutiona. Otherwise you will see an error!
  - use the Django deployment checklist, especially update DEBUG and ALLOWED_HOSTS
  - "When we installed `environs[django]` earlier, the Django “goodies” included the elegant `dj-database-url129` package, which takes all the database configurations needed for our database, SQLite or PostgreSQL. This will be very helpful later on in production."

### 10. email; adding a dedicated 3party provider
  - "email_confirmation_- message.txt file located within django-allauth/allauth/templates/account/email. If you look at this directory’s content there is also a subject line file, email_confirmation_message.txt that we can and will change.
  - To customize these files we’ll override them by recreating the same structure of django-allauth in our project. That means creating an email directory within the templates/account directory."
  - internalization functionality helps support multiple languages
  - autoescape template tag is automatically on and protects against XSS
  - site name is in the `sites` section of the Django admin, used by `django-allauth`
  - set `DEFAULT_FROM_EMAIL` in `settings.py`
  - The locations of the `django-allauth` default password reset and password change pages are as follows: • http://127.0.0.1:8000/accounts/password/reset/
                        • http://127.0.0.1:8000/accounts/password/change/
  - when ready to use a real email server, add `EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"` to `settings.py` and configure EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_- PASSWORD, EMAIL_PORT, and EMAIL_USE_TLS based on the instructions from your email provider as environment variables.

### 11. models, tests, pages for bookstore via `books` app
  - new app workflow: `docker-compose exec web python manage.py startapp newapp`; then add `newapp` to INSTALLED_APPS in `settings.py`
  - in a model, the __str__ method controls how the object is outputted in Admin and Django shell.
  - to change what fields you want displayed in a certain list of admin objects, alter the admin file with a new `list_display` attribute for your class, and register the class and admin with the site, e.g.
    - `class BookAdmin(admin.ModelAdmin):
      - list_display = ("title", "author", "price",)
      - admin.site.register(Book, BookAdmin)`
  - Once a database model is complete, we need to create the necessary views, URLs, and templates. We can display the information on our Web application. WSV recommends starting with the URLs, then the views, then the templates.
  - `ListView` is a Generic Class-Based View provided for common use cases like this. All we must do is specify the proper model and template to be used.
  - Django automatically adds an auto-incrementing primary key to our database models, called `id` and accessed with either `id` or `pk`. We can then cast this as an integer and use it in routes, e.g.
    - `path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),` where we use the universal id of a book as its path
    - `pk` is more reliable than `id` for this since it signifies primary key, whereas `id` can be changed
  - in a template, we can showcase the page title in title tags so it appears on the browser tab label, e.g.
    - {% block title %}{{ object.title }}{% endblock title %}
  - Just as ListView defaults to object_list which we updated to be more specific, so too DetailView defaults to object which we can make more descriptive using context_object_name.
  - `get_absolute_url` method sets a canonical URL for a model, and is required when usiing the `reverse()` function.
  - "Using the pk field in the URL of our DetailView is quick and easy, but not ideal for a real-world project. The pk is currently the same as our auto-incrementing id. Among other concerns, it tells a potential hacker exactly how many records you have in your database; it tells them exactly what the id is which can be used in a potential attack; and there can be synchronization issues if you have multiple front-ends."
    - instead, use a slug - a short URL label, or better yet a UUID, Universally Unique
  - If you create a UU ID for all existing entries in your database, a new migration would cause serious problems. Instead, simply delete old migrations and start over.
    - `docker-compose exec web rm -r books/migrations`

### 12. addition of reviews to bookstore; FOREIGN KEYS, app structure, forms
  - Three kinds of foreign key relatonships
    - **One-to-one** - rare in practice, unusual for both sides to only match with one counterpart, but examples are country-flag or person-passport
    - **One-to-many** - more common, also the default foreign key setting within Django. Example is person-payments. 
    - **Many-to-many** - examples are a list of books and list of authors, where any number of authors can write a book and each author can write more than one book. Another example is doctors and patients, since each doctor sees multiple patients and vice versa, or employees and tasks
  - **Normalization** is the process of structuring a relational database
  - simplest reviews implementation is a one-to-many between authors and reviews
  - standard practice is to name the one-to-many foreign key after the linked model, i.e. the `book` field in the Books -> `Review` model is a one-to-many key that links reviews to books, and its `related_name` is "reviews". As well, we will populate the author field in reviews. related_name must be unique.
  - Django does not store raw passwords which means even as a superuser we cannot see individual user passwords. We can change the password to something else but we can’t just copy and paste user passwords. All passwords are encrypted by default.
  
### 13. image uploading
  - Django refers to static files as `static` whereas anything uploaded by a user, whether it be a file or an image, is referred to as `media`. This is because we can trust the former by default, but not the latter. Important to validate all uploaded files, since a bad actor can attack a site blindly accepting uploads.
  - For this case we need the Python image processing lib Pillow. 
  - Two `settings.py` configurations that default to empty and not displayed:
    - `MEDIA_ROOT` is the absolute file system path to the directory for user-uploaded files 
    - `MEDIA_URL` is the URL we can use in our templates for the files
  - since user-uploaded content is assumed to exist in a production context, to see media items locally we need to update `django_project/urls.py` to show the files locally. This involves importing both `settings` and `static` at the top and then adding an additional line at the bottom.
    - `cover = models.ImageField(upload_to="covers/")`
  - It’s common to see blank and nulla used together to set a default value on a field. A gotcha is that the field type – ImageField vs. CharField and so on – dictates how to use them properly so closely read the documentation for future use.
  - We must add some basic logic to our template so that if a cover is not present the template doesn’t look for it!
    - `{% if book.cover %}<img class="bookcover" src="{{ book.cover.url}}" alt="{{ book.title }}">{% endif %}`
  - Steps that a truly production website could take: storing all media files on a dedicated CDN (Content Delivery Network) rather than its our own server. The popular third-party package django-storages178 allows for storing Django media files on a service like Amazon’s S3.
  - "Heroku has an ephemeral file system179. Each internal dyno boots with a clean copy of the file system from the most recent deploy. Static files are located on the file system; media files are not. As a result, in production media files will not remain with Heroku. Using django-storages is therefore basically mandatory alongside Heroku and will be mentioned again in the deployment chapter."

### 14. site permissions; lockdown
  - "Django comes with built-in authorization options for locking down pages to either logged in users, specific groups, or users with the proper individual permission. Confusingly there are multiple ways to add even the most basic permission: restricting access only to logged-in users. It can be done in a raw way using the `login_required()` decorator, or since we are using class-based views so far via the `LoginRequired` mixin."
  - It is important that `LoginRequiredMixin` come before `ListView` in order to work properly. Mixins are powerful but can be a little tricky in practice. As the official docs note, “not all mixins can be used together, and not all generic class based views can be used with all other mixins.
  - It's common to set custom permissions using the `Meta` class of database models:
    - `class Meta: # new permissions = [
            ("special_status", "Can read all books"),
        ]
    -Once these attributes are defined for a class, they can be easily changed using Django admin panel
  - we also use `PermissionRequiredMixin` and `UserPassesTestMixin` in this section
  - In large projects Groups, Django's way of applying permissions to a category of users, become prominent, with a dedicated `Groups` section on the admin page which makes setting permissions much easier. An example is premium users.
    - Note that you also must test these permissions heavily in order to make sure the site still works and has desired behavior

### 15. complex search
  - a **QuerySet** is used to filter the results from a database model.
    - contains and icontains are easy filters to implement in a queryset, e.g.
      - `queryset = Book.objects.filter(title__icontains="beginners")`
    - For basic filtering most of the time the built-in queryset methods of `filter()`, `all()`, `get()`, or `exclude()` will be enough. However there is also a very robust and detailed QuerySet API available as well
  - You can chain filters, but dfor a more complex lookup that can use "OR" and not just "AND", you'll need to turn to Q objects.
  - There are only two options for “how” a form is sent: either via GET or POST HTTP methods.
    - A POST bundles up form data, encodes it for transmission, sends it to the server, and then receives a response. Any request that changes the state of the database–creates, edits, or deletes data– should use a POST.
    - A GET bundles form data into a string that is added to the destination URL. GET should only be used for requests that do not affect the state of the application, such as a search where nothing within the database is changing, basically we’re 
    just doing a filtered list view.
  - Main search infra:
    - urls.py:
      -     path("search/", SearchResultsListView.as_view(), name="search_results"),
    - views.py:
      - def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    - base.html:
      -                 <form class="d-flex" action="{% url 'search_results' %}" method="get">
                    <input class="form-control me-2" type="search" name="q" placeholder="Search" aria-\ label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>

### 16. performance optimizations via `django-debug-toolbar` to inspect queries/templates, database indexes, front-end assets, multiple built-in caching options
  - Django performance comes down to four major areas: optimizing database queries, caching, indexes, and compressing front-end assets like images, JavaScript, and CSS.
  - use `django-debug-toolbar` comes with a configurable set of panels for inspecting the complete requuest/response cycle of any page.
    - Needs to be configured iin `INSTALLED_APPS`, Middleware, and `INTERNAL_IPS`.
    - For setup on a web server withiin docker, additional infra at end of `settings.py to ensure INTERNAL_IPS matches that of our docker host:
      - #django-debug-toolbar
        import socket
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
  - Django for Professionals book page there are six queries being run:
    - the sessions framework215 to manage users
    - to accounts_customuser to load our user
    - to books_book to load the “Django for Professionals” book • to books_review to load the reviews
    - and then 2 more queries to accounts_customuser
  - Count and label queries on one page using the debug toolbar, flag duplicates, reduce queries
  - There are two powerful methods included in the Django ORM to help us that can boost performance by creating a single more complex QuerySet rather than multiple, smaller queries:
    - `select_related` for Foreign Key relationships, returns a QuerySet that follows foreign-key relationships, either 1to1 or manytomany, selecting additional related-object data as needed. The RM creates a SQL jin and includes the fields of a related object in the `SELECT` statement, so all related objects are included in a single more complex DB query
    - `prefetch_related()` for Many to Many relationships. Separate lookup for each relationship and “joins” them together with Python, not SQL. This allows it to prefetch many-to-many and many-to-one objects, which cannot be done using `select_related`
    - QuerySets are unique and lazy
    - In a QuerySet, a double underscore denotes a lookup, commonly used to filter Querysets, e.g.
      - queryset = Book.objects.all().prefetch_related("reviews__author",)
    - **indexing**, a common technique for improving DB performance, is a separate data structure that allows faster searches and is typically only applied to the primary key in a model. The downside is that indexes require additional space on a disk so they must be used with care.
      - if a given field is being used frequently, such as 10-25% of all queries, it is a prime candidate to be indexed. It's best to include this syntax in the `Meta` section, e.g.
        - class Meta:
            indexes = [ # new
              models.Index(fields=["id"], name="id_index"),
            ]
            permissions=[("special_status", "Can read all books"),]
  - **caching** - Django has its own cache framework which includes four different caching options in descending order of granularity:
    1) The per-site cache233 is the simplest to set up and caches your entire site.
    2) The per-view cache234 lets you cache individual views.
    3) Template fragment caching235 lets you specify a specific section of a template to cache.
    4) The low-level cache API236 lets you manually set, retrieve, and maintain specific objects in the cache.
    - As a site grows in size, a dedicated and separate caching server often makes sense. The two most popular options for this are Redis and Memcached which, as of Django 4.0, both come with built-in Django support.
    - There are also several third-party packages that can be helpful in identifying N+1 issues, most notably nplusone, django-zen-queries, and django-auto-prefetch.

### 17. Security in Django, native and 3party
  - Best practices: Keep project and packages up-to-date (even monthly security patches), restrict user permissions except where absolutely necessary. it's unwise to use Django's Long-Term Support(LTS) versions and better to update.
  - Django features deprecation warnings that can and should be run for each new release by typing `python -Wa manage.py test`
  - Use the deployment checklist! or even better, you can automate thiis with the command `python manage.py check --deploy`
    - this will show a list of typically 6**issues**, with typical ones below
  - create a separate `docker-compose-prod.yml` file to contain production details, then IMMEDIATELY add to .gitignore
    - **Issue 1** set DEBUG false here to eliminate an issue with deploy
    - default all settings in this file to the moost secure, production-only options
  - To run our new file, spin down the Docker container and restart it via the -f flag to specify an alternate compose file. By default, Docker assumes a `docker-compose.yml` so adding the -f flag is unnecessary in that case.
    - specifically, `docker-compose -f docker-compose-prod.yml up -d`
  - Terminal command to tell Python package `secrets` to make a new secret key:
    - `docker-compose exec web python -c "import secrets; print(secrets.token_urlsafe(38))"`
    - **Issue 2** Take this key and copy into `docker-compose-prod.yml`
  - **Issue 3** - set a secure SSL redirect in `settings.py`
    - `SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)`
    - Then add the env variable to docker-compse.yml, so that for local development it defaults to the less secure False.
    - "Companies typically actually have three different environments set up: one for local, one for production, and a staging server that mimics production but allows for more actual testing before switching things over completely. Going forward if you want to try out the local website with production settings be aware you will have to toggle off DJANGO_SECURE_SSL_REDIRECT."
  - **Issue 4** There are three implicit HSTS configurations in our settings.py file that need to be updated for production:
    - `SECURE_HSTS_SECONDS = 0` -> 2592000, 30 days, the greater the better for security purposes
    - `SECURE_HSTS_INCLUDE_SUBDOMAINS = False` -> True, force subdomains to use SSL
    - `SECURE_HSTS_PRELOAD = False` -> True, only works when there's a nonzero value for SECURE_HSTS_SECONDS
    - so e.g. actual sample code in settings.py:
      - SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)
      - SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
         "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
        )
      -SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
    - and e.g. actual vars in Docker-compose (not prod):
      - "DJANGO_SECURE_HSTS_SECONDS = 0"
      - "SECURE_HSTS_INCLUDE_SUBDOMAINS = False"
      - "SECURE_HSTS_PRELOAD = False"
  - **Issue 5 and 6** Secure cokiies - HTTP protocol is stateless by design; no way to tell if a user is authenticated ther than an including an identifier in the HTTP header. So cookies store thiis info on the client's computer
    - "Django uses sessions and cookies for this, as do most websites. But cookies can and should be forced over HTTPS as well via the SESSION_COOKIE_SECURE config. By default Django sets this value to False for local development; in production it needs to be True."
    - "The second issue is CSRF_COOKIE_SECURE293, which defaults to False but in production should be True so that only cookies marked as “secure” will be sent with an HTTPS connection."
    - As befre, two new vars in `settings.py`:
      - SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
      - CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
    - And two in docker-compose.yml, under web/environment:
      - "DJANGO_SESSION_COOKIE_SECURE=False"
      - "DJANGO_CSRF_COOKIE_SECURE=False"
  - **extra issue: strengthening Django Admin**
    - change the admin url to something else so it's not so easily accessible. You can simply change the URL pattern in urls.py of your project.
  - Summary: "By using a docker-compose-prod.yml file we can accurately test, within Docker, our production settings before deploying the site live. And by using default values we can both simplify the environment variables in the file as well as ensure that if something goes awry with environment variables we will default to secure production values."
### 18. Deployment, upgrades to migrate from Django webserver, local static file handling, `ALLOWED_HOSTS`
  - " A PaaS is an opinionated hosting option that handles much of the initial configura- tion and scaling needed for a website. Popular examples include Heroku298, PythonAnywhere299, and Dokku300 among many others. While a PaaS costs more money upfront than an IaaS it saves an incredible amount of developer time, handles security updates automatically, and can be quickly scaled."
  - "An IaaS by contrast provides total flexibility and is typically cheaper, but it requires a high degree of knowledge and effort to properly set up. Prominent IaaS options include DigitalOcean301, Linode302, Amazon EC2303, and Google Compute Engine304 among many others."
  - IaaS is more cmplex and varies widely in configuration
  - We use WhiteNoise to help serve static files to Heroku; search `settings` to see changes
  - "django_project/wsgi.py file was created with a default WSGI (Web Server Gateway Interface)310 configuration. This is a specification for how a web app (like our Bookstore project) communicates with a web server. For production it is common to swap this out for either Gunicorn311 or uWSGI312. Both offer a performance boost, but Gunicorn is more focused and simpler to implement so it will be our choice."
    - to use Gunicorn, add to requirements and the following to Dockerfile/command:
      - command: gunicorn bookstore.wsgi -b 0.0.0.0:8000
  - Traditional non-Docker Heroku relies on a custom Procfile for configuring a site for deployment. For containers Heroku relies on a similar approach but it is called a heroku.yml file.

  ### Other Django Docs I read for this project
  - - [Django Testing Documentation](https://docs.djangoproject.com/en/4.0/topics/testing/)
- [Python Unittest Library](https://docs.python.org/3/library/unittest.html)
- [GitHub Code Quality Features](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
- [Django TemplateView](https://docs.djangoproject.com/en/4.0/ref/class-based-views/base/#django.views.generic.base.TemplateView)
- [Django URL Resolvers](https://docs.djangoproject.com/en/4.0/ref/urlresolvers/#resolve)
- [Django QuerySets - Last](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#last)
- [SWR - React Hooks Library](https://swr.vercel.app/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/)
- [Django-Allauth GitHub Repository](https://github.com/pennersr/django-allauth)
- [Bootstrap Getting Started Guide](https://getbootstrap.com/docs/3.3/getting-started/)
- [Bootstrap and jQuery Error Solution on StackOverflow](https://stackoverflow.com/questions/22658015/bootstrap-throws-uncaught-error-bootstraps-javascript-requires-jquery)
- [GitHub Writing and Formatting Syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Bootstrap CDN via jsDelivr](https://getbootstrap.com/docs/5.1/getting-started/download/#cdn-via-jsdelivr)
- [Django LOGIN_REDIRECT_URL](https://docs.djangoproject.com/en/4.0/ref/settings/#login-redirect-url)
- [Django Authentication Views](https://docs.djangoproject.com/en/5.0/topics/auth/default/#all-authentication-views)
- [Django URL Naming Patterns](https://docs.djangoproject.com/en/5.0/topics/http/urls/#naming-url-patterns)
- [Django URL Template Tag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#url)
- [Django Authentication Data in Templates](https://docs.djangoproject.com/en/5.0/topics/auth/default/#authentication-data-in-templates)
- [Django Templates Variables](https://docs.djangoproject.com/en/5.0/topics/templates/#variables)
- [Django Contrib Auth Views](https://docs.djangoproject.com/en/5.0/topics/auth/default/#module-django.contrib.auth.views)
- [Django Allauth Tutorial](https://learndjango.com/tutorials/django-allauth-tutorial)
- [Google Docs - Django Notes](https://docs.google.com/document/d/1hxh15XP5_MdLedztperwfdTIAPiIZAfK7QXkhhEvYlc/edit#heading=h.ongxlgib2mah)
- [Docker Command Line Exec](https://docs.docker.com/engine/reference/commandline/exec/)
- [The Twelve-Factor App](https://12factor.net/)
- [Django SECRET_KEY Setting](https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SECRET_KEY)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/)
- [Django Internationalization](https://docs.djangoproject.com/en/4.0/topics/i18n/)
- [Django Autoescape Tag](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#autoescape)
- [Django UUIDField](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.UUIDField)
- [Django setUpTestData](https://docs.djangoproject.com/en/5.0/topics/testing/tools/#django.test.TestCase.setUpTestData)
- [Django TabularInline](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.TabularInline)
- [Django MEDIA_ROOT Setting](https://docs.djangoproject.com/en/5.0/ref/settings/#media-root)
- [Django MEDIA_URL Setting](https://docs.djangoproject.com/en/5.0/ref/settings/#media-url)
- [Django Permissions and Authorization](https://docs.djangoproject.com/en/4.0/topics/auth/default/#permissions-and-authorization)
- [Django Model Style Guide](https://docs.djangoproject.com/en/4.0/internals/contributing/writing-code/coding-style/#model-style)
- [Django Retrieving Objects](https://docs.djangoproject.com/en/4.0/topics/db/queries/#retrieving-objects)
- [Django Other QuerySet Methods](https://docs.djangoproject.com/en/4.0/topics/db/queries/#other-queryset-methods)
- [Django QuerySet API](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#queryset-api)
- [MDN Web Docs - Sending and Retrieving Form Data](https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data)
- [MDN Web Docs - Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)
- [Django Postgres Search](https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/)
- [Django Debug Toolbar Documentation](https://django-debug-toolbar.readthedocs.io/en/latest/index.html)
- [Django select_related QuerySet](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#select-related)
- [Django prefetch_related QuerySet](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#prefetch-related)
- [Django QuerySets Documentation](https://docs.djangoproject.com/en/4.0/ref/models/querysets/)
- [Django Filtered QuerySets](https://docs.djangoproject.com/en/4.0/topics/db/queries/#filtered-querysets-are-unique-1)
- [Django Lazy QuerySets](https://docs.djangoproject.com/en/4.0/topics/db/queries/#querysets-are-lazy-1)
- [Django Caching Framework](https://docs.djangoproject.com/en/4.0/topics/cache/)
- [Django Version Upgrade Guide](https://docs.djangoproject.com/en/4.0/howto/upgrade-version/)
- [Django Security](https://docs.djangoproject.com/en/4.0/topics/security/)
- [Django Storages Documentation](https://django-storages.readthedocs.io/en/latest/)
- [Django Debug Toolbar Display Issues](https://django-debug-toolbar.readthedocs.io/en/latest/tips.html#the-toolbar-isn-t-displayed)
- [Django Debug Toolbar Forum Discussion](https://forum.djangoproject.com/t/django-debug-toolbar-not-showing-up/14092/16)
- [Tmuxinator GitHub Repository](https://github.com/tmuxinator/tmuxinator)
- [Django REST Framework Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django REST Framework Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [Django REST Framework Homepage](https://www.django-rest-framework.org/#example)
