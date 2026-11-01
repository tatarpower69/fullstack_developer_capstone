import json
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .models import CarMake

def index(request): return render(request, 'index.html')
def about(request): return render(request, 'About.html')
def contact(request): return render(request, 'Contact.html')

def payload(request):
    try:
        value = json.loads(request.body)
        return value if isinstance(value, dict) else {}
    except (ValueError, UnicodeError):
        return {}

def identity(user):
    return {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name} if user.is_authenticated else None

@require_GET
def csrf(request): return JsonResponse({'csrfToken': get_token(request)})

@require_GET
def user(request): return JsonResponse({'user': identity(request.user)})

@require_POST
def login_user(request):
    data = payload(request)
    account = authenticate(request, username=data.get('username', ''), password=data.get('password', ''))
    if account is None: return JsonResponse({'error': 'Invalid username or password'}, status=401)
    login(request, account)
    return JsonResponse({'status': 'Authenticated', 'user': identity(account)})

@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({'status': 'Logged out'})

@require_POST
def register(request):
    data = payload(request)
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    if any(not isinstance(data.get(key), str) or not data[key].strip() for key in fields):
        return JsonResponse({'error': 'All five fields are required'}, status=400)
    account = User(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    try:
        account.full_clean(exclude=['password'])
        validate_password(data['password'], account)
        account.set_password(data['password'])
        account.save()
    except (ValidationError, IntegrityError):
        return JsonResponse({'error': 'Use a unique username, valid email, and password with at least 8 characters'}, status=400)
    login(request, account)
    return JsonResponse({'user': identity(account)}, status=201)

def upstream(path, method='get', data=None):
    try:
        response = requests.request(method, settings.DEALERS_URL + path, json=data, headers={'X-Service-Token': settings.SERVICE_TOKEN}, timeout=8)
        return JsonResponse(response.json(), safe=False, status=response.status_code)
    except (requests.RequestException, ValueError):
        return JsonResponse({'error': 'Dealership service is temporarily unavailable'}, status=503)

@require_GET
def dealers(request, state=None):
    from urllib.parse import quote
    return upstream('/fetchDealers' + ('/' + quote(state, safe='') if state else ''))

@require_GET
def dealer(request, dealer_id): return upstream(f'/fetchDealer/{dealer_id}')

@require_GET
def reviews(request, dealer_id): return upstream(f'/fetchReviews/{dealer_id}')

def sentiment(text):
    response = requests.get(settings.SENTIMENT_URL + '/analyze', params={'text': text}, timeout=8)
    response.raise_for_status()
    return response.json()['sentiment']

@require_POST
def add_review(request):
    if not request.user.is_authenticated: return JsonResponse({'error': 'Please sign in'}, status=401)
    data = payload(request)
    try:
        data['dealership'] = int(data.get('dealership', 0))
        data['car_year'] = int(data.get('car_year', 0))
        if not 1900 <= data['car_year'] <= 2100 or not 1 <= len(data.get('review', '').strip()) <= 5000:
            raise ValueError()
        data['name'] = request.user.get_full_name() or request.user.username
        data['sentiment'] = sentiment(data['review'])
    except (ValueError, TypeError): return JsonResponse({'error': 'Enter a review and valid vehicle year'}, status=400)
    except (requests.RequestException, KeyError): return JsonResponse({'error': 'Sentiment service is unavailable'}, status=503)
    return upstream('/insert_review', 'post', data)

@require_GET
def cars(request):
    return JsonResponse({'car_models': [{'id': model.id, 'car_make': make.name, 'car_model': model.name, 'year': model.year, 'type': model.type} for make in CarMake.objects.prefetch_related('models') for model in make.models.all()]})

@require_GET
def analyze(request):
    text = request.GET.get('text', '')
    if not text: return JsonResponse({'error': 'text is required'}, status=400)
    try: return JsonResponse({'text': text, 'sentiment': sentiment(text)})
    except requests.RequestException: return JsonResponse({'error': 'Sentiment service is unavailable'}, status=503)
