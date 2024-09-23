from .base import *  # noqa
from config.env import env


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", str)


ALLOWED_HOSTS = ["*"]
