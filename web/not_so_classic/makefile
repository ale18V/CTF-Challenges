SHELL := /bin/bash
all: down clean build up

down:
	docker-compose down

clean:
	sudo rm -f app/db/app.db
	sudo rm -rdf app/src/static/uploads/*
build: 
	gcc -o app/run/run app/run/run.c
	docker-compose build

up:	
	docker-compose up

distribute:
	rm -rdf dist
	bash scripts/redact.sh
