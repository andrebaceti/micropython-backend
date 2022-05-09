"""Check registration endpoints."""
import requests
import unittest
from pumpwood_communication.microservices import PumpWoodMicroService


class TestRegistrationAPI(unittest.TestCase):
    load_balancer_address = 'http://localhost:8080/'
    apps_to_regenerate = ['micropython-backend-app']
    session = requests.session()
    session.headers.update(
        {'Authorization': 'Token 6cab4ba54bb8f92af7e135d7ad8c7d70d4555f7f'})
    auth_header = {
        'Authorization': 'Token 6cab4ba54bb8f92af7e135d7ad8c7d70d4555f7f'}

    session = requests.session()
    session.headers.update(
        {'Authorization': 'Token 6cab4ba54bb8f92af7e135d7ad8c7d70d4555f7f'})

    load_balancer_address = "http://0.0.0.0:8080/"
    'Ip of the load balancer'
    apps_to_regenerate = ['micropython-backend-app']
    'Name of the apps to be regenerated after the test is over'

    test_address = "http://0.0.0.0:5000/"

    def setUp(self, *args, **kwargs):
        """Regen the database in the setUp calling reload end-point."""
        ######################
        # Regenerate database#
        for app in self.apps_to_regenerate:
            path = 'reload-db/' + app + '/'
            response = requests.get(self.load_balancer_address + path)
            if response.status_code != 200:
                raise Exception(app + ' regenerate: ', response.text)
