all: down clean build up

down:
	docker-compose down

clean:
	sudo rm -rdf app/src/__pycache__
	sudo rm -rdf app/db/app.db

build:
	gcc -o app/run/run app/run/run.c
	docker-compose build

up:	
	docker-compose up
