FROM python:3.8-buster

# Cloud deploy envs
ENV CLOUD="TRUE"
ENV PYTHONUNBUFFERED="1"

# Database
ENV DB_NAME="pumpwood"
ENV DB_USERNAME="pumpwood"
ENV DB_PASS="pumpwood"
ENV DB_HOST="test-db-pumpwood-auth"
ENV DB_PORT="5432"
ENV N_WORKERS="10"
ENV SIGNUP = "FALSE"

# Microservice
ENV MICROSERVICE_NAME='microservice-auth'
ENV MICROSERVICE_NOLOGIN_NAME="microservice-auth_nologin"
ENV MICROSERVICE_URL="http://load-balancer:8000/"
ENV MICROSERVICE_USERNAME='microservice--auth'
ENV MICROSERVICE_PASSWORD='microservice--auth'
ENV MICROSERVICE_SSL='False'

# Service Mesh registration
ENV SERVICE_URL="http://micropython-backend-app:5000/"
ENV API_GATEWAY_URL="http://load-balancer:8001/"
ENV AUTH_STATIC_SERVICE="http://pumpwood-auth-admin-static:5000/"
ENV TEST_RELOADDB_SERVICE="http://test-db-pumpwood-auth:5000/"

# Packages install
COPY requirements/requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt

# Postgres dependencies
RUN apt-get update
RUN apt-get install -y postgresql-client

# Coping files
COPY django /django
WORKDIR /django/

CMD ["bash", "/django/start_server.sh"]
