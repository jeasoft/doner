# online key generator:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'my-super-secret-generated-key'

LANGUAGE_CODE = 'en-us'

DEFAULT_FROM_EMAIL = 'doner <doner@myproject.com>'

SITE_URL = 'http://doner.myproject.com'


# ### PostgreSQL ###
#
# REMEMBER TO:
#    $ pip install psycopg2
#
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

# ### MySQL ###
#
# REMEMBER TO:
#   $ pip install MySQL-python
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

# ### SQLite ###
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
