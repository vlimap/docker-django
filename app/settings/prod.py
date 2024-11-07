from .base import *
import environ

# Inicializando o django-environ
env = environ.Env()
# Configurações específicas para o ambiente de produção
DEBUG = False
SECRET_KEY = env('SECRET_KEY')  # A chave secreta deve vir do ambiente

# Banco de Dados em produção
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # O SQLite armazenará os dados no arquivo db.sqlite3
    }
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# CORS para produção
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

# Outras configurações específicas de produção (ex: uso de cache, balanceamento, etc.)
