up:
	docker-compose up
up_bg:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build
api:
	docker-compose exec api bash
db:
	docker-compose exec db psql --username=postgres
.PHONY: up up_bg down build api db
