# sudoku

#steps to setup 

Make sure that you have *not* run `pipenv shell` yet, then run these two commands:

```
cd website
pipenv install
```

If you accidentally ran `pipenv shell` before those two commands, you should exit the shell using CTRL+d. Then run the two commands.

Now, you activate the virtual environment by typing the following command in the directory of the project:

```
pipenv shell
```

now first change the code at settings.py file at 'sudoku' folder
at line near 95 in 
DATABASES = {
...
}
comment out all content inside DATABASES block
and copy paste :
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',  # left empty means defult port is used which is 5432 while installing
    }
    
now your DATABASES will look like :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',  # left empty means defult port is used which is 5432 while installing
    }
}

then 

If this is your first time creating a local version of the website for testing, you'll need to set up the local website database from scratch. The following command will create a new database with the models in the Outreachy website. The database will initially have no website pages, but will eventually store your local test pages.

```
./python manage.py migrate
```

The next step is to create an admin account for the local website.

```
./python manage.py createsuperuser
```

then to run server :
./python manage.py runserver


