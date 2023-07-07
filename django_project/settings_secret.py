import os
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = 'django-insecure-1$$$(9*&_!2w&f0&xen$i(3gbj$t%lrz(+eg4^oee4gr_w@3^6'

EMAIL_HOST_USER = os.environ.get('DB_HOST_GMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('DB_HOST_GMAIL_PASS')

EMAIL_PORT = 587