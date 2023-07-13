# sudoku PRO - Completed
# sudoku
this is a web application for gaming sudoku(watchting ranks, user stats visualization using plots)  and solver that checks validity of sudoku puzzle and can solve any valid sudoku puzzle

# Demo of the APPLICATION : 

https://github.com/sh-Shubham17/sudokuPro/assets/61670651/47769502-4d84-4f93-82d9-eb8fb23cee46


## Updation : 
plots for visualition of user improvement and stats

https://github.com/sh-Shubham17/sudokuPro/assets/61670651/4af147c0-6fda-45d2-9589-22f7084825c3


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
'default': {
   'ENGINE': 'django.db.backends.postgresql_psycopg2',
   'NAME': 'postgres',
   'USER': 'postgres',
   'PASSWORD': '1234',
   'HOST': 'localhost',
   'PORT': '5432',  # left empty means defult port is used which is 5432 while installing.
  }
```
</br></br>
now your DATABASES will look like :</br>
```
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
```
</br>
then </br>
If this is your first time creating a local version of the website for testing, you'll need to set up the local website database from scratch. The following command will create a new database with the models in the sudoku app. The database will initially have no website pages, but will eventually store your local test pages.

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
