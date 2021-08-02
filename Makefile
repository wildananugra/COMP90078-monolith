compose-up:
	@docker-compose up -d --build --remove-orphans
	
compose-down:
	@docker-compose down

run-app:
	@uvicorn main:app --reload --host 0.0.0.0 --port 8080

run-db:
	@docker run --name comp90078-pg -p 5432:5432 -v data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=comp90078! -e POSTGRES_USER=comp90078 -e POSTGRES_DB=comp90078-db -d postgres