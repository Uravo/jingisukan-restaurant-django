import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_env_file(path):
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env_file(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-dev-secret-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in {"1", "true", "yes", "on"}
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver,japaninsight.uz,www.japaninsight.uz").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


JAZZMIN_SETTINGS = {
    "site_title": "Jingisukan Admin",
    "site_header": "Jingisukan Izakaya",
    "site_brand": "Jingisukan",
    "site_logo": "assets/images/logo.jpg",
    "login_logo": "assets/images/logo.jpg",
    "site_icon": "assets/images/logo.jpg",
    "site_logo_classes": "img-circle elevation-2",
    "custom_css": "css/jazzmin_light.css",
    "welcome_sign": "Welcome to Jingisukan Izakaya back office",
    "copyright": "Jingisukan Izakaya",
    "search_model": ["core.Booking", "core.BlogPost"],
    "topmenu_links": [
        {"name": "Website", "url": "/en/", "new_window": True},
        {"name": "Bookings", "url": "/backoffice/bookings/"},
        {"name": "Blog Posts", "url": "/backoffice/posts/"},
    ],
    "icons": {
        "core.Booking": "fas fa-calendar-check",
        "core.BlogPost": "fas fa-newspaper",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-light-primary",
    "accent": "accent-primary",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success",
    },
}
