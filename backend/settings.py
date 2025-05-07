"""
settings.py – Konfigurácia Django backend projektu SCADA systému

Tento súbor obsahuje všetky nastavenia projektu vrátane:
- registrácie aplikácií
- databázového pripojenia
- middleware
- timezone
- REST frameworku a CORS politiky

Dokumentácia: https://docs.djangoproject.com/en/5.2/topics/settings/
"""

from pathlib import Path

# Absolútna cesta k adresáru projektu
BASE_DIR = Path(__file__).resolve().parent.parent


# 🛡️ BEZPEČNOSŤ A LADENIE

SECRET_KEY = 'django-insecure-9=y+1&0gygja1l$-98@j412bz&4b60&f(bsx3la-2g77@1@eq+'
DEBUG = True  # ⚠️ V produkcii vždy nastaviť na False
ALLOWED_HOSTS = []  # V produkcii pridať IP/domény servera


# 📦 REGISTRÁCIA APLIKÁCIÍ

INSTALLED_APPS = [
    'corsheaders',              # povolenie CORS pre frontend
    'rest_framework',           # Django REST API podpora
    'plc',                      # vlastná aplikácia pre PLC a senzory
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# 🔄 MIDDLEWARE – vrstvy spracovania požiadaviek

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🌐 SMEROVANIE A ŠABLÓNY

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # tu môžeš pridať cestu k vlastným HTML šablónam
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# 💾 DATABÁZA – SQLite pre vývojové prostredie

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔐 VALIDÁCIA HESIEL

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 🌍 LOKALIZÁCIA A ČASOVÉ PÁSMA

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Bratislava'
USE_I18N = True
USE_TZ = False  # ❗ Ak zaznamenávaš čas z PLC priamo, ponechaj False


# 🖼️ STATICKÉ SÚBORY (CSS, JS, obrázky)

STATIC_URL = 'static/'


# 🆔 PRIMÁRNE KĽÚČE

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 🌐 CORS – povolenie pre všetky domény (frontend na inom porte)

CORS_ALLOW_ALL_ORIGINS = True


# 🧰 DJANGO REST FRAMEWORK – výstup len v JSON formáte

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
