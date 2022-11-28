## Stripe

Приложение представляет собой сервер с возможностью выбирать товары и оплачивать их 
с помощью платёжной системы [Stripe](https://stripe.com/docs/checkout/quickstart).
Посмотреть рабочий пример можно [здесь](http://89.223.127.50:8000/).

Перед запуском, нужно **установить** 
[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) и 
[docker-compose](https://docs.docker.com/compose/install/).

### .env - файл с переменными окружения
В корне проекта нужно создать файл .env, 
и заполнить его необходимыми для работы приложения переменными. Пример .env файла:
```
DEBUG=True

# порт для приложения
PORT=8000

# движок базы данных
POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2

# имя базы данных
POSTGRES_DB=stripe_db

# пользователь базы данных
POSTGRES_USER=postgres

# пароль базы данных
POSTGRES_PASSWORD=pg_pass

# хост базы данных
POSTGRES_HOST=db

# порт базы данных
POSTGRES_PORT=5432

# секретный ключ django (https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key)
SECRET_KEY=django_secret_key_0123456789

# домен хоста, где запущено приложение
DOMAIN=http://127.0.0.1:8000

# публичный и приватный ключи для stripe
STRIPE_PUBLIC_KEY=pk_test_0123456789
STRIPE_SECRET_KEY=sk_test_0123456789
```

### Запуск приложения 
Здесь будут описаны прямые команды, а также через утилиту 
[make](https://habr.com/ru/post/211751/):
#### Через make:
```bash
make run
```
#### Прямая команда:
```bash
docker-compose build
docker-compose up
```

### Создать superuser для django-admin:
#### Через make:
```bash
make superuser
```
#### Прямая команда:
```bash
docker exec -it stripe_app python manage.py createsuperuser
```
