run: build up

makemig:
	python manage.py makemigrations

migrate:
	docker exec stripe_app python manage.py migrate

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

superuser:
	docker exec -it stripe_app python manage.py createsuperuser
