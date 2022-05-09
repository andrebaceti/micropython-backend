"""Login tests."""
import requests
import unittest


class TestLoginCases(unittest.TestCase):
    """Test user login."""

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

    def test__correct_login(self):
        """Check login."""
        url = 'http://localhost:8000/' + 'rest/registration/login/'
        response_1 = requests.post(url, json={
                "username": "pumpwood-estimation-app",
                "password": "pass:12345-estimation-app"})
        response_1.raise_for_status()

    def test__incorrect_login(self):
        """Check login error."""
        url = 'http://localhost:8000/' + 'rest/registration/login/'
        response_1 = requests.post(url, json={
                "username": "pumpwood-estimation-app",
                "password": "password-errado"})
        self.assertEqual(response_1.status_code, 400)
        resp_data = response_1.json()
        self.assertEqual(
            resp_data["message"],
            'Username/Password incorrect')

    def test__blank_password(self):
        """Check error response for blank password."""
        url = 'http://localhost:8000/' + 'rest/registration/login/'
        response_1 = requests.post(url, json={
            "username": "user1",
            "password": ""})
        self.assertEqual(response_1.status_code, 400)
        resp_data = response_1.json()
        self.assertEqual(
            resp_data["message"], 'Username/Password incorrect')

    def test__none_password(self):
        """Check error response for None password."""
        url = 'http://localhost:8000/' + 'rest/registration/login/'
        response_1 = requests.post(url, json={
            "username": "user1",
            "password": None})
        self.assertEqual(response_1.status_code, 400)
        resp_data = response_1.json()
        self.assertEqual(
            resp_data["message"], 'Username/Password incorrect')

    # def check_token_refreshing(self):
    #     """Check if token if refreshing."""
    #     url = 'http://localhost:8000/' + 'rest/registration/login/'
    #     response_1 = requests.post(url, json={
    #             "username": "pumpwood-estimation-app",
    #             "password": "pass:12345-estimation-app"})
    #     ex_token = response_1.json()['token']
    #
    #     response_1 = requests.post(url, json={
    #             "username": "pumpwood-estimation-app",
    #             "password": "pass:12345-estimation-app"})
    #     new_token = response_1.json()['token']
    #     self.assertNotEqual(ex_token, new_token)

    def check_token_not_refreshing_microservice(self):
        """Check if token if not refreshing for microservice."""
        url = 'http://localhost:8000/' + 'rest/registration/login/'
        resp_microservice1 = self.session.post(
            url, json={
                "username": "microservice--auth",
                "password": "microservice--auth"})
        response = resp_microservice1.json()
        ex_token = response['token']

        resp_microservice1 = self.session.post(
            '/rest/registration/login/', {
                "username": "microservice1",
                "password": "microservice1"},
            format='json')
        new_token = resp_microservice1.data['token']
        self.assertEqual(ex_token, new_token)

    def test__check_logged(self):
        """Check if user is logged."""
        # Ordinary user check
        response = requests.post(
            'http://0.0.0.0:8000/rest/registration/login/', json={
                "username": "user1", "password": "pass:12345-user1"})
        response.raise_for_status()
        response_data = response.json()

        new_header = {
            "Authorization": 'Token ' + response_data['token']}
        check = requests.get(
            'http://0.0.0.0:8000/rest/registration/check/',
            headers=new_header)
        check.raise_for_status()
        check_data = check.json()
        self.assertTrue(check_data)

    def test__check_logged_microservice(self):
        """Check if microservice is logged."""
        # Microservice check
        response = self.session.post(
            'http://0.0.0.0:8000/rest/registration/login/', json={
                "username": "microservice--auth",
                "password": "microservice--auth"})
        response.raise_for_status()
        response_data = response.json()

        new_header = {
            "Authorization": 'Token ' + response_data['token']}
        check = self.session.get(
            'http://0.0.0.0:8000/rest/registration/check/',
            headers=new_header)
        check.raise_for_status()
        self.assertTrue(check.json())

    def test__logout_and_check(self):
        """Check user logout."""
        # Ordinary user check
        response = self.session.post(
            'http://0.0.0.0:8000/rest/registration/login/', json={
                "username": "user1", "password": "pass:12345-user1"})
        response.raise_for_status()
        response_data = response.json()

        new_header = {
            "Authorization": 'Token ' + response_data['token']}
        response_logout = self.session.get(
            'http://0.0.0.0:8000/rest/registration/logout/',
            headers=new_header)
        response_logout.raise_for_status()

        response_check = self.session.get(
            'http://0.0.0.0:8000/rest/registration/check/',
            headers=new_header)
        self.assertEqual(response_check.status_code, 401)

    def test__logout_and_check_microservice(self):
        """Check microservice logout."""
        # Microservice check
        response = self.session.post(
            'http://0.0.0.0:8000/rest/registration/login/', json={
                "username": "microservice1",
                "password": "pass:12345-nao-deixa-o-pass"})
        response.raise_for_status()
        response_data = response.json()

        new_header = {
            "Authorization": 'Token ' + response_data['token']}
        response_logout = self.session.get(
            'http://0.0.0.0:8000/rest/registration/logout/',
            headers=new_header)

        response_check = self.session.get(
            'http://0.0.0.0:8000/rest/registration/check/',
            headers=new_header)
        self.assertEqual(response_check.status_code, 401)
