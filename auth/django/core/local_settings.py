import os

# Os servidores locais são os end points, servem as
# aplicações que não precisam de outros servidores
django_db_name = os.environ.get('DB_NAME')
django_db_username = os.environ.get('DB_USERNAME')
django_db_pass = os.environ.get('DB_PASS')
django_db_host = os.environ.get('DB_HOST')
django_db_port = os.environ.get('DB_PORT')

DEBUG = os.environ.get('DEBUG', 'FALSE') == 'TRUE'
ADMINS = (
)

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': django_db_name,
        # Not used with sqlite3.
        'USER': django_db_username,
        # Not used with sqlite3.
        'PASSWORD': django_db_pass,
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': django_db_host,
        # Set to empty string for default. Not used with sqlite3.
        'PORT': django_db_port,
    }
}
ALLOWED_HOSTS = ('*')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '8540')


#######################
# Email Configuration #
#######################
# Email configuration. If you are using gmail's smtp make sure to activate
# this configuration:
# https://support.google.com/accounts/answer/6010255
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'

# Use {username} and {activation_link} in the email message template to place
# the username and activation link respectively. See the example below.
SIGNUP_ACTIVATION_EMAIL_MESSAGE_TEMPLATE = ""
SIGNUP_ACTIVATION_EMAIL_SUBJECT = ""
# Use {activation_key} in the redirect link to place the activation key.
# See the example below.
SIGNUP_ACTIVATION_REDIRECT_LINK = ""

# its is the same to reset password
RESET_PASSWORD_EMAIL_MESSAGE_TEMPLATE = ""
RESET_PASSWORD_EMAIL_SUBJECT = ""
RESET_PASSWORD_REDIRECT_LINK = ""
