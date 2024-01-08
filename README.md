
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
  -
### 15. complex search
### 16. performance optimizations via `django-debug-toolbar` to inspect queries/templates, database indexes, front-end assets, multiple built-in caching options
### 17. Security in Django, native and 3party
### 18. Deployment, upgrades to migrate from Django webserver, local static file handling, `ALLOWED_HOSTS`