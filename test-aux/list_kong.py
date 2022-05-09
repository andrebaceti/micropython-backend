import os
from pumpwood_kong.kong import KongManagement


SERVICE_URL = os.environ.get("SERVICE_URL")
API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL")
AUTH_STATIC_SERVICE = os.environ.get("AUTH_STATIC_SERVICE")
TEST_RELOADDB_SERVICE = os.environ.get("TEST_RELOADDB_SERVICE")

kong_statup_obj = KongManagement(
    api_gateway_url=API_GATEWAY_URL)
