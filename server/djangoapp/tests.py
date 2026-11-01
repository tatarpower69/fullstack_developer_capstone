import json
from unittest.mock import patch, Mock
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel

class AccountTests(TestCase):
    def setUp(self): self.client = Client(enforce_csrf_checks=True)
    def post(self, path, data):
        token = self.client.get('/djangoapp/csrf').json()['csrfToken']
        return self.client.post('/djangoapp/' + path, json.dumps(data), content_type='application/json', HTTP_X_CSRFTOKEN=token)
    def test_register_login_logout_and_invalid_password(self):
        fields = {'username':'driver', 'first_name':'Test', 'last_name':'Driver', 'email':'driver@example.com', 'password':'A-test-password-349!'}
        self.assertEqual(self.post('registration', fields).status_code, 201)
        self.assertFalse(User.objects.get(username='driver').password == fields['password'])
        self.assertEqual(self.client.get('/djangoapp/user').json()['user']['username'], 'driver')
        self.assertEqual(self.post('logout', {}).status_code, 200)
        self.assertIsNone(self.client.get('/djangoapp/user').json()['user'])
        self.assertEqual(self.post('login', {'username':'driver','password':'wrong'}).status_code, 401)
        self.assertEqual(self.post('login', fields).status_code, 200)
    def test_csrf_and_review_auth_are_enforced(self):
        self.assertEqual(self.client.post('/djangoapp/login', '{}', content_type='application/json').status_code, 403)
        self.assertEqual(self.post('add_review', {}).status_code, 401)
    def test_invalid_registration_and_duplicate(self):
        self.assertEqual(self.post('registration', {}).status_code, 400)
        fields = {'username':'driver', 'first_name':'Test', 'last_name':'Driver', 'email':'driver@example.com', 'password':'A-test-password-349!'}
        self.assertEqual(self.post('registration', fields).status_code, 201)
        self.assertEqual(self.post('registration', fields).status_code, 400)
    @patch('djangoapp.views.requests.request')
    @patch('djangoapp.views.sentiment', return_value='positive')
    def test_review_author_comes_from_session(self, sentiment, proxy):
        user=User.objects.create_user('driver',password='test-pass-123',first_name='Real',last_name='Driver')
        self.client.force_login(user)
        proxy.return_value=Mock(status_code=201,json=lambda:{'review':{'name':'Real Driver'}})
        response=self.post('add_review',{'dealership':1,'car_year':2025,'review':'Fantastic services','name':'Forged author'})
        self.assertEqual(response.status_code,201)
        self.assertEqual(proxy.call_args.kwargs['json']['name'],'Real Driver')
    def test_car_catalog(self):
        make=CarMake.objects.create(name='Toyota')
        CarModel.objects.create(car_make=make,name='Camry')
        self.assertEqual(self.client.get('/djangoapp/get_cars').json()['car_models'][0]['car_make'],'Toyota')
    @patch('djangoapp.views.requests.request')
    def test_dealer_service_failure_is_reported(self, proxy):
        import requests
        proxy.side_effect=requests.ConnectionError()
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code,503)
