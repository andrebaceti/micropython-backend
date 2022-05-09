docker-compose rm -f
source docker-versions.env
COMPOSE_HTTP_TIMEOUT=200 docker-compose up --force-recreate --remove-orphans > docker.log
