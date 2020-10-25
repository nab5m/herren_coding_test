from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "herren_prod",
        "USER": "herren_prod",
        "PASSWORD": "nab5m!_!",
        "HOST": "db",
        "PORT": "5432",
    }
}
