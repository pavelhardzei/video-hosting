up:
	docker-compose up
up_bg:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build
auth:
	docker-compose exec auth bash
db:
	docker-compose exec db psql --username=postgres
.PHONY: up up_bg down build auth db
