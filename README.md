doner
=====

Ticket Management System for Getting Things Done™ (TMS4GTD)

[<img src="http://i.imgur.com/bohNGBhl.png" width="250">](http://imgur.com/bohNGBhl)
[<img src="http://i.imgur.com/WqtXNtbl.png" width="250">](http://imgur.com/WqtXNtb)

Installation
============

Get the code
------------

    $ git clone git@github.com:trojkat/doner.git

Setup virtualenv
----------------

    $ cd doner
    $ pip install --upgrade virtualenv
    $ virtualenv env
    $ source env/bin/activate

Install requirements
--------------------

    ./setup.py develop

Create local settings file
--------------------------

Create `settings_local.py` file next to `settings.py`.

    $ cd doner
    $ cp doner/settings_local_example.py doner/settings_local.py


Edit `doner/settings_local.py` file and customize settings.


Setup database
--------------

    $ ./manage.py syncdb
    $ ./manage.py create superuser

Run app
-------

    $ ./manage.py runserver

Django admin panel is available under `/admin/` url.
