# run local pg db in docker
docker run --name local-postgres -e POSTGRES_PASSWORD=Aa123456 -d -p 5432:5432 postgres