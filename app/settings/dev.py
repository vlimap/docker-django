from decouple import config
from .base import *

# Configurações específicas para o ambiente de desenvolvimento
DEBUG = config('DEBUG', default=True, cast=bool)  # Se o DEBUG for False, precisa de ALLOWED_HOSTS
SECRET_KEY = config('SECRET_KEY')

# Configuração do Banco de Dados para o ambiente de desenvolvimento
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Usando SQLite para desenvolvimento
    }
}

# Configuração de ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = ['localhost']  # Para desenvolvimento, só aceita localhost
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')  # Para produção, lido do .env

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
