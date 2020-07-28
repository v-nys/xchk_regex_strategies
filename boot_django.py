# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

def boot_django():
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=(
            "xchk_core",
            "xchk_regex_strategies",
        ),
        AUTH_USER_MODEL="django.contrib.auth.models.User"
    )
    django.setup()
