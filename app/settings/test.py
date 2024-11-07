from .base import *
import environ

# Inicializando o django-environ
env = environ.Env()
# Configurações específicas para o ambiente de testes
DEBUG = True  # Pode ser True em ambiente de teste, mas nunca em produção
SECRET_KEY = 'test_secret_key'

# Banco de Dados de Teste
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # O SQLite armazenará os dados no arquivo db.sqlite3
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Configurações de CORS para testes
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']

# Outras configurações de teste (como cobertura, logging de erros, etc.)
