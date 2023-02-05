
create_env:
	cat .env.template > .env

build: create_env
	docker-compose build

run: build
	docker-compose up -d

run_db: build
	docker-compose up -d db

stop:
	docker-compose down

test: build
	docker-compose run web pytest
