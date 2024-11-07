Este arquivo explica passo a passo como configurar as variáveis de ambiente, como configurar os Dockerfiles, fazer o "freeze" dos requisitos e como subir os ambientes de desenvolvimento, produção e teste.

# Django with Docker

Este projeto contém uma aplicação Django configurada com Docker para ambientes de desenvolvimento, produção e teste. Abaixo estão as etapas para configurar, rodar e desenvolver o projeto em diferentes ambientes.

## Estrutura do Projeto

```plaintext
C:\Windows\System32\docker-django
│
├── app/                    # Código do Django
│   ├── settings/           # Configurações do Django
│   │   ├── __init__.py     # Inicializa o pacote de configurações
│   │   ├── base.py         # Configurações base
│   │   ├── dev.py          # Configurações para ambiente de desenvolvimento
│   │   ├── prod.py         # Configurações para ambiente de produção
│   │   ├── test.py         # Configurações para ambiente de teste
│   ├── __init__.py
│   ├── asgi.py             # Arquivo ASGI
│   ├── wsgi.py             # Arquivo WSGI
│
├── Dockfile/               # Dockerfiles para cada ambiente
│   ├── Dockerfile.dev      # Dockerfile para ambiente de desenvolvimento
│   ├── Dockerfile.prod     # Dockerfile para ambiente de produção
│   ├── Dockerfile.test     # Dockerfile para ambiente de teste
│
├── requirements/           # Arquivos de requisitos de pacotes Python
│   ├── requirements-dev.txt # Requisitos para desenvolvimento
│   ├── requirements-prod.txt # Requisitos para produção
│   ├── requirements-test.txt # Requisitos para teste
│
├── .dockerignore           # Arquivo para ignorar arquivos ao criar a imagem Docker
├── .env.dev                # Variáveis de ambiente para desenvolvimento
├── .env.prod               # Variáveis de ambiente para produção
├── .env.test               # Variáveis de ambiente para teste
├── docker-compose.yml      # Definição dos containers e serviços do Docker
├── manage.py               # Script de gerenciamento do Django
└── README.md               # Este arquivo
```

## Configuração das Variáveis de Ambiente

Este projeto utiliza o `django-environ` e `python-decouple` para carregar as variáveis de ambiente. A configuração é feita por meio de arquivos `.env`.

### Arquivos `.env`

Existem três arquivos de configuração para as variáveis de ambiente, um para cada ambiente:

- `.env.dev` - Para desenvolvimento
- `.env.prod` - Para produção
- `.env.test` - Para testes

Exemplo de como configurar o `.env.dev`:

```ini
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_DATABASE=your_database_name
DB_USERNAME=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Carregando as Variáveis

Dentro das configurações do Django, usamos `django-environ` e `python-decouple` para ler essas variáveis de ambiente.

```python
from decouple import config
import environ

# Inicializando django-environ
env = environ.Env()

DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
```

## Dockerfiles

O projeto possui Dockerfiles específicos para cada ambiente:

- `Dockerfile.dev`: Usado para construir a imagem de desenvolvimento.
- `Dockerfile.prod`: Usado para construir a imagem de produção.
- `Dockerfile.test`: Usado para construir a imagem de teste.

Exemplo do Dockerfile de Desenvolvimento (`Dockerfile.dev`):

```dockerfile
# Use a imagem oficial do Python
FROM python:3.11-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos de dependências
COPY requirements/requirements-dev.txt /app/requirements.txt

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Expor a porta do Django (8000 por padrão)
EXPOSE 8000

# Comando para iniciar o Django em modo de desenvolvimento
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Requirements

Use `pip freeze` para gerar um arquivo `requirements.txt` com todas as dependências do seu projeto. Cada ambiente tem um arquivo de requisitos correspondente:

Para desenvolvimento, gere o arquivo `requirements-dev.txt`:

```bash
pip freeze > requirements/requirements-dev.txt
```

Para produção, gere o arquivo `requirements-prod.txt`:

```bash
pip freeze > requirements/requirements-prod.txt
```

Para testes, gere o arquivo `requirements-test.txt`:

```bash
pip freeze > requirements/requirements-test.txt
```

## Docker Compose

O Docker Compose é utilizado para orquestrar os containers do Django e PostgreSQL. O arquivo `docker-compose.yml` configura os seguintes serviços:

- Django (web): Serviço principal, rodando o servidor Django.
- PostgreSQL (db): Banco de dados PostgreSQL.

Exemplo do arquivo `docker-compose.yml`:

```yaml
version: "3.9"

services:
    web:
        build:
            context: .
            dockerfile: Dockfile/Dockerfile.dev  # Use o Dockerfile correto
        volumes:
            - .:/app
        ports:
            - "8000:8000"
        environment:
            - DEBUG=True
            - SECRET_KEY=your_secret_key_here
            - DB_HOST=db
            - DB_PORT=5432
            - DB_DATABASE=your_database_name
            - DB_USERNAME=your_database_user
            - DB_PASSWORD=your_database_password
        depends_on:
            - db

    db:
        image: postgres:13
        environment:
            POSTGRES_USER: your_database_user
            POSTGRES_PASSWORD: your_database_password
            POSTGRES_DB: your_database_name
        volumes:
            - postgres_data:/var/lib/postgresql/data

volumes:
    postgres_data:
```

## Subindo os Ambientes

### Para Desenvolvimento

Para rodar o ambiente de desenvolvimento, use o Docker Compose para criar e iniciar os containers:

```bash
docker-compose up --build
```

Esse comando vai construir as imagens e iniciar os containers para o ambiente de desenvolvimento.

### Para Produção

Para rodar o ambiente de produção, você precisará usar o Dockerfile de produção:

```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Para Testes

Similar ao ambiente de produção, você pode rodar o ambiente de teste usando o Dockerfile de teste:

```bash
docker-compose -f docker-compose.test.yml up --build
```

## Cenário: Atualizando um Docker em Produção com Novas Atualizações

Assumindo que você já tem um Docker em produção em execução, e agora você tem novas atualizações que foram testadas em uma branch de desenvolvimento, aqui está o fluxo recomendado para subir essas atualizações de forma segura:

### 1. Preparar o Ambiente de Produção

Antes de atualizar a produção, você precisa garantir que tudo esteja preparado para receber as mudanças. Aqui estão as verificações e etapas preliminares:

**Passo 1: Certifique-se de que o ambiente de produção está estável**

- Verifique se a aplicação está rodando corretamente no ambiente de produção antes de aplicar as mudanças.
- Se você estiver usando Docker Compose, verifique se os containers estão em funcionamento e se o banco de dados está acessível.

**Passo 2: Faça backup do banco de dados**

IMPORTANTE: Antes de qualquer atualização em produção, sempre faça um backup completo do banco de dados. Isso garante que, se algo der errado, você poderá restaurar a versão anterior.

No caso de PostgreSQL, por exemplo, você pode fazer isso com o comando:

```bash
docker exec -t <container_postgres> pg_dumpall -c -U postgres > backup.sql
```

### 2. Atualizar a Branch de Produção

Você tem a sua aplicação rodando com o código em produção, mas agora precisa atualizar esse código com as novas mudanças que você fez em uma branch.

**Passo 3: Verifique a branch de produção**

- Certifique-se de que a branch de produção esteja atualizada.
- Caso você tenha feito as alterações em uma branch de desenvolvimento ou feature, você precisa mesclar essas alterações na branch de produção (geralmente chamada de main, master ou prod).

No seu repositório, faça isso com os seguintes comandos:

```bash
git checkout prod  # ou 'main', 'master', conforme o nome da sua branch de produção
git pull origin prod  # para garantir que a branch de produção local esteja atualizada
git merge <sua-branch-de-desenvolvimento>  # ou 'feature-branch', dependendo do nome
git push origin prod  # envie a nova atualização para o repositório remoto
```

Nota: Caso você tenha atualizações no banco de dados (por exemplo, novas migrações do Django), é importante garantir que o código da branch de produção também tenha as novas migrações.

### 3. Atualizar a Imagem Docker de Produção

Agora que você tem as mudanças aplicadas à branch de produção, o próximo passo é reconstruir a imagem Docker e colocar a nova versão em produção.

**Passo 4: Reconstruir a Imagem Docker para Produção**

- Reconstruir a imagem Docker de produção. No diretório onde está o seu Dockerfile.prod, execute o seguinte comando para construir a imagem Docker com as últimas atualizações:

```bash
docker build -t nome_da_imagem:latest -f Dockerfile.prod .
```

- Recriar os containers usando a nova imagem. Para isso, no caso de estar utilizando o Docker Compose, basta fazer:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

O `--build` garante que as alterações feitas no código sejam aplicadas ao container, e o `-d` fará com que os containers rodem em segundo plano.

**Passo 5: Verificar se os containers foram atualizados corretamente**

- Verifique se os containers estão sendo reconstruídos e reiniciados com a nova imagem. Você pode verificar os logs do Docker para garantir que não há problemas.

```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Executar as Migrações de Banco de Dados

Se as suas atualizações incluírem mudanças no banco de dados (novas tabelas, alterações de schema, etc.), você precisará rodar as migrações do Django.

**Passo 6: Executar as migrações de banco de dados**

- No container em que o Django está rodando, execute as migrações do banco de dados com o comando:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

Isso aplica todas as migrações pendentes e garante que o banco de dados esteja atualizado de acordo com o código novo.

### 5. Verificação Pós-Deploy

Após as mudanças estarem no ar, é importante verificar se a aplicação está funcionando corretamente.

**Passo 7: Testar a aplicação em produção**

- Acesse a aplicação em produção e verifique se a nova versão está funcionando como esperado.
- Faça uma verificação completa dos endpoints e funcionalidades principais para garantir que o sistema está respondendo corretamente.
- Se estiver usando um balanceador de carga (por exemplo, nginx ou AWS ELB), verifique também o tráfego para garantir que não há interrupções.

### 6. Rollback (Se necessário)

Se algo der errado após o deploy, você pode reverter para a versão anterior. Existem algumas formas de fazer isso:

**Passo 8: Rollback para a versão anterior**

Caso precise reverter para a versão anterior, você pode:

- Reverter o código da branch de produção (voltar para o commit anterior):

```bash
git checkout prod
git reset --hard <commit-antigo>
git push -f origin prod
```

- Reconstruir a imagem Docker com a versão anterior:

```bash
docker build -t nome_da_imagem:antiga -f Dockerfile.prod .
docker-compose -f docker-compose.prod.yml up -d --build
```

- Executar as migrações de rollback (se necessário, dependendo do tipo de migração realizada).

Caso você tenha feito migrações de banco de dados, você pode reverter para o estado anterior rodando migrações de rollback (como desfazer migrações no Django, se necessário):

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate app_name <migration_name>
```

Ou, se não houver mais migrações anteriores, você pode rodar a reversão de migração do Django.

### Resumo do Fluxo para Atualização em Produção

**Prepare o ambiente:**

- Verifique se a aplicação está estável e faça backup do banco de dados.

**Atualize a branch de produção:**

- Mescle as alterações de desenvolvimento na branch de produção e faça o push.

**Reconstrua a imagem Docker de produção:**

- Use o docker-compose para construir e subir os novos containers.

**Execute migrações do banco de dados:**

- Aplique as migrações de banco de dados usando o Django.

**Teste a aplicação:**

- Verifique se a aplicação está funcionando corretamente no ambiente de produção.

**Rollback (se necessário):**

- Caso algo dê errado, faça o rollback da versão anterior.

## Estratégias para Atualizar a Aplicação em Produção sem Downtime

A principal estratégia para garantir que a aplicação continue funcionando enquanto a nova versão é implantada é usar a abordagem de rolling updates ou blue-green deployment. Vamos ver como essas estratégias funcionam:

### 1. Rolling Update com Docker

Um rolling update permite atualizar as instâncias da aplicação uma por uma, sem que todas as instâncias sejam interrompidas ao mesmo tempo. Isso é ideal para sistemas com múltiplos containers ou instâncias.

**Passo 1: Recriar Containers Gradualmente**

Se você estiver usando o Docker Compose com múltiplos containers ou um sistema de orquestração como o Docker Swarm ou Kubernetes, você pode configurar a atualização de containers para que uma nova instância seja criada enquanto a antiga ainda está em execução. A aplicação não será interrompida, pois sempre haverá pelo menos uma instância disponível.

Com o Docker Compose, você pode realizar o deploy sem downtime da seguinte forma:

- Reconstruir a imagem Docker com as novas alterações: Se você fez mudanças no código, no Dockerfile, ou em qualquer outro lugar, reconstrua a imagem Docker.

```bash
docker-compose -f docker-compose.prod.yml build
```

- Subir a nova versão sem interromper os containers atuais: Você pode usar a opção `up` com a flag `--no-deps` para evitar que dependências sejam recriadas, garantindo que a aplicação continue rodando enquanto os containers são atualizados.

```bash
docker-compose -f docker-compose.prod.yml up -d --no-deps --build
```

O Docker irá atualizar a aplicação, mas sem parar os containers que estão em funcionamento.

**Passo 2: Verificar o Processo de Atualização**

Verifique se os novos containers estão sendo criados e se os antigos continuam rodando até que os novos containers estejam prontos.

Você pode monitorar o status dos containers com o comando:

```bash
docker ps
```

Ou ver os logs de saída para garantir que a aplicação está respondendo corretamente:

```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### 2. Blue-Green Deployment

No blue-green deployment, você mantém duas versões da aplicação: a versão "blue" (atualmente em produção) e a versão "green" (a nova versão que você deseja colocar no ar). O tráfego de produção é redirecionado da versão blue para a versão green sem downtime.

**Passo 1: Configurar a versão Blue (Atual em Produção)**

Sua aplicação blue está funcionando e serve todas as requisições de produção.

**Passo 2: Criar uma Nova Versão Green**

Você cria e configura a versão green com as novas alterações no código. Isso pode ser feito em uma nova imagem Docker, como explicamos anteriormente.

**Passo 3: Rodar os Contêineres Green Paralelamente**

Faça a criação dos containers da versão green. Isso pode ser feito sem interromper os containers da versão blue:

```bash
docker-compose -f docker-compose.green.yml up -d
```

Agora você tem ambas as versões rodando em paralelo.

**Passo 4: Redirecionar o Tráfego para a Versão Green**

Quando a versão green estiver funcionando corretamente, você pode alterar o balanceador de carga (caso tenha um) ou alterar as configurações de rede para direcionar o tráfego da versão blue para a versão green.

No caso de nginx ou outro proxy reverso, você só precisa alterar a configuração de proxy para apontar para os containers da versão green.

**Passo 5: Eliminar a Versão Blue**

Uma vez que você tenha redirecionado o tráfego para a versão green e verificado que a aplicação está funcionando como esperado, você pode derrubar os containers da versão blue:

```bash
docker-compose -f docker-compose.blue.yml down
```

## Considerações Finais

- **Variáveis de ambiente**: Garanta que o arquivo `.env` correto esteja sendo utilizado em cada ambiente (dev, prod, test).
- **Requisitos**: Não se esqueça de "congelar" suas dependências com `pip freeze` para manter a consistência entre os ambientes.
- **Docker Compose**: O Docker Compose facilita a orquestração dos serviços do Django e do banco de dados PostgreSQL.
- **Segurança**: Para produção, nunca deixe variáveis sensíveis no código ou em arquivos públicos (como o `.gitignore`).

Esse README fornece uma visão geral das etapas para configurar, desenvolver e executar seu projeto Django com Docker em diferentes ambientes.
