source version
PGPASSWORD=pumpwood pg_dump -h localhost -p 7000 -U pumpwood pumpwood > db_dump/database.sql
docker build -t andrebaceti/test-db-micropython-backend:${VERSION} .
rm db_dump/database.sql
