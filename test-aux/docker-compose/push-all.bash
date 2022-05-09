source docker-versions.sh

docker push andrebaceti/test-db-micropython-backend:$TEST_DB_MICROPYTHON_APP
docker push andrebaceti/micropython-backend-app:$MICROPYTHON_APP
docker push andrebaceti/micropython-backend-static:$MICROPYTHON_STATIC
