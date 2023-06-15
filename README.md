# sudoku PRO - Completed

## steps to setup 

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
</br></br>
now first change the code at settings.py file at 'sudoku' folder</br>
at line near 95 in </br>
DATABASES = {</br>
...</br>
}</br>
comment out all content inside DATABASES block</br>
and copy paste :</br>
```
'default': {</br>
   'ENGINE': 'django.db.backends.postgresql_psycopg2',</br>
   'NAME': 'postgres',</br>
   'USER': 'postgres',</br>
   'PASSWORD': '1234',</br>
   'HOST': 'localhost',</br>
   'PORT': '5432',  # left empty means defult port is used which is 5432 while installing.</br>
  }</br>
```
</br></br>
now your DATABASES will look like :</br>
```
DATABASES = {</br>
 'default': {</br>
     'ENGINE': 'django.db.backends.postgresql_psycopg2',</br>
     'NAME': 'postgres',</br>
     'USER': 'postgres',</br>
     'PASSWORD': '1234',</br>
     'HOST': 'localhost',</br>
     'PORT': '5432',  <> left empty means defult port is used which is 5432 while installing</br><
  }</br>
}</br>
```
</br>
then </br>
If this is your first time creating a local version of the website for testing, you'll need to set up the local website database from scratch. The following command will create a new database with the models in the Outreachy website. The database will initially have no website pages, but will eventually store your local test pages.

```
./python manage.py migrate
```
</br>
The next step is to create an admin account for the local website.

```
./python manage.py createsuperuser
```
</br>
then to run server :

```
./python manage.py runserver
```


