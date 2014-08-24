doner
=====

Ticket Management System for Getting Things Done™ (TMS4GTD)

[<img src="http://i.imgur.com/WqtXNtbl.png" style="width:250px">](http://imgur.com/WqtXNtb)
[<img src="http://i.imgur.com/bohNGBhl.png" style="width:250px">](http://imgur.com/bohNGBhl)

Installation
============

Setup virtualenv
----------------

    $ pip install --upgrade virtualenv
    $ virtualenv env
    $ source env/bin/activate

Get the code
------------

    $ git clone git@github.com:trojkat/doner.git

Install requirements
--------------------

    $ cd doner
    ./setup.py develop

Create local settings file
--------------------------

Create `settings_local.py` file next to `settings.py`.

    $ touch doner/doner/settings_local.py


set new secret key ([secret key generator](http://www.miniwebtool.com/django-secret-key-generator/))

    SECRET_KEY = 'SOME_NEW_SECRET_KEY'

database settings ([see more](https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-DATABASES))

    # PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

Setup database
--------------

    $ ./manage.py syncdb
    $ ./manage.py create superuser

Run app
-------

    $ ./manage.py runserver
