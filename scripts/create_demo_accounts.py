"""Create local demonstration accounts; generated passwords stay in ignored private data."""
import json
import os
import secrets
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'server'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','dealership.settings')
import django
django.setup()
from django.contrib.auth.models import User
private=ROOT/'evidence/private'
private.mkdir(parents=True,exist_ok=True)
path=private/'accounts.json'
accounts=json.loads(path.read_text()) if path.exists() else {name:secrets.token_urlsafe(20) for name in ['capstone_driver','capstone_admin']}
for username,password in accounts.items():
    account,created=User.objects.get_or_create(username=username,defaults={'first_name':'Ilnur' if username=='capstone_driver' else 'Demo','last_name':'Driver' if username=='capstone_driver' else 'Administrator','email':username+'@example.com','is_staff':username=='capstone_admin','is_superuser':username=='capstone_admin'})
    if created: account.set_password(password);account.save()
path.write_text(json.dumps(accounts,indent=2))
print('Local demo accounts ready. Passwords are in ignored evidence/private/accounts.json.')
