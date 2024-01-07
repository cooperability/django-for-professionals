Django for Professionals by William Vincent - Detailed Notes

    Chapter 1: Local Setup, Venv, Command Line, Git, Python
        Django is a scaling ORM (object-relational-mapper) database, meaning we will use almost identical Django code for any one of several possible databases like PostgreSQL, MariaDB, Oracle, MySQL, and SQLite. The Django ORM handles the translation from Python code to SQL configured for each database automatically.
        Used to create Instagram, Spotify, and Dropbox.
        Best practice is to use the same database locally and in production, making Django's built-in sqlite3 database unsuitable for most production-ready apps.
        Django loads apps from top-to-bottom, so generally good practice is adding new apps below built-in apps they rely on like admin, auth, etc.
        django-admin startproject <projectname>.
        cd into new folder created and run python manage.py startapp <appname> to create a new app.
        You then need to add the appname to the list of installed apps in the settings.py file in the subfolder for your main app.
        Structure:
            __init__.py just tells python to treat it like a python directory.
            settings.py has the program guts & backend.
            asgi.py and wsgi.py don't need to be edited, but dictate how the program interacts with a browser.
            urls allows you to determine route.
            manage.py allows you to make db migrations, run the server, etc.
        It's not advisable to run migrations before configuring a custom user model. If you do so, Django will bind the database to the built-in user model, which is difficult to modify later on in the project.
        In app folder:
            Admin allows you to register database models so they can be viewed from the admin panel.
            Models where you dictate those models.
            Apps you don't need to worry about.
            Views allows you to create routes on the website.
        Terminal Commands:
            cd into project; add django.
            django-admin startproject <projectname>.
            cd <projectname>.
            python manage.py startapp myapp.
            Django will create files but not recognize the new app until added to the INSTALLED_APPS config in settings.py.
            python manage.py runserver.
            python manage.py makemigrations.
            python manage.py migrate.
            ALWAYS create a custom user model before you make your initial migration; if you don't, there will be more complicated problems down the line. Steps to add:
                Create CustomUser model.
                Update django_project/settings.py.
                Customize UserCreationForm and UserChangeForm.
                Add custom user model to admin.py.
                Create a function call for your user model in settings.py so it can be referenced identically across your project, e.g., in settings.py, AUTH_USER_MODEL = "accounts.CustomUser".
                In forms.py, class Meta: model=get_user_model.
            The password field is implicitly included in all users by default; we need to extend the AbstractUser class that Django provides.
            python manage.py createsuperuser.
            python manage.py runserver.