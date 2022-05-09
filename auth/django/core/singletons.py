"""Define singletons objects for django app."""
import os
from pumpwood_communication.microservices import PumpWoodMicroService


MICROSERVICE_NAME = os.environ.get("MICROSERVICE_NAME")
MICROSERVICE_URL = os.environ.get("MICROSERVICE_URL")
MICRO_DJANGO_USERNAME = os.environ.get("MICRO_DJANGO_USERNAME")
MICRO_DJANGO_PASSWORD = os.environ.get("MICRO_DJANGO_PASSWORD")
microservice = PumpWoodMicroService(
    name=MICROSERVICE_NAME, server_url=MICROSERVICE_URL,
    username=MICRO_DJANGO_USERNAME, password=MICRO_DJANGO_PASSWORD,
    verify_ssl=False)
