
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
### 7. Static asset configuration for CSS, JS, images, Bootstrap
### 8. Advanced user reg; email-only login & social auth via `django-allauth` 3party package
### 9. environment variables
### 10. email; adding a dedicated 3party provider
### 11. models, tests, pages for bookstore via `books` app
### 12. addition of reviews to bookstore; FOREIGN KEYS
### 13. image uploading
### 14. site permissions; lockdown
### 15. complex search
### 16. performance optimizations via `django-debug-toolbar` to inspect queries/templates, database indexes, front-end assets, multiple built-in caching options
### 17. Security in Django, native and 3party
### 18. Deployment, upgrades to migrate from Django webserver, local static file handling, `ALLOWED_HOSTS`