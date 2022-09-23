up:
	docker-compose up
up_bg:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build
auth:
	docker-compose exec -it auth bash
auth_db:
	docker-compose exec -it auth_db psql -U postgres
content:
	docker-compose exec -it content bash
content_db:
	docker-compose exec -it content_db psql -U postgres
.PHONY: up up_bg down build auth auth_db content content_db
