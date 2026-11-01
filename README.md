# Cars Dealership

Repository: **cars-dealership-capstone**  
Project: **Cars Dealership — Full-stack Development Capstone**

A responsive dealership directory with account registration, session login/logout, vehicle catalog, dealership details, customer reviews, sentiment labels, and Django administration.

## Architecture

- **React + Vite** renders the directory, state filtering, authentication, and reviews.
- **Django + SQLite** owns accounts, sessions, CSRF protection, the vehicle catalog, and the API gateway.
- **Node.js + MongoDB** stores dealers and reviews. A durable JSON adapter is available for local development when MongoDB is not installed; it is not a MongoDB deployment.
- **Flask** provides a deterministic local sentiment baseline with negation handling. It is explicitly not IBM Watson or a trained AI model.
- Docker Compose connects the three services and MongoDB. GitHub Actions checks Django, runs tests, and builds React.

All dealership records, contact information, team profiles, and initial reviews are demonstration data. Team photos are illustrative Unsplash images. This project was prepared with AI assistance; disclose that assistance according to course rules.

## Local setup (Python 3.12+ and Node 22+)

```powershell
python -m pip install -r requirements.txt
cd server/frontend
npm ci
npm run build
cd ../..
python server/manage.py migrate
python server/manage.py seed_cars
python scripts/create_demo_accounts.py
python scripts/run_local.py
```

Open http://127.0.0.1:8000. The admin is at `/admin/`. Generated demo passwords are stored only in ignored `evidence/private/accounts.json`; never commit that file. You can also register a new account in the browser or run `python server/manage.py createsuperuser`.

## Docker / MongoDB

Copy `.env.example` to `.env` and replace both secret placeholders with independently generated values, then run `docker compose up --build`. The MongoDB and microservice ports are internal to the Compose network. SQLite and MongoDB use persistent named volumes. Docker must be running.

The development Compose configuration intentionally binds only to localhost. Before a public deployment, configure production settings, HTTPS, a stable secret, static file serving, trusted hosts and CSRF origins, and persistent storage. See [Django’s deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

## API

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/djangoapp/csrf` | GET | Obtain a CSRF token |
| `/djangoapp/registration` | POST | Register with username, first/last names, email, password |
| `/djangoapp/login` | POST | Start an authenticated session |
| `/djangoapp/logout` | POST | End the session |
| `/djangoapp/get_dealers` | GET | List dealerships |
| `/djangoapp/get_dealers/Kansas` | GET | Filter by state |
| `/djangoapp/dealer/1` | GET | Dealer details |
| `/djangoapp/reviews/dealer/1` | GET | Dealer reviews |
| `/djangoapp/get_cars` | GET | Car makes and models |
| `/djangoapp/add_review` | POST | Add a review (login + CSRF required) |
| `/djangoapp/analyze_review?text=Fantastic%20services` | GET | Sentiment result |

## Validation and submission evidence

```powershell
python server/manage.py check
python server/manage.py test djangoapp
python -m unittest discover -s services/sentiment
```

`evidence/` contains only actual captured command results or screenshots. Missing CI/cloud results must remain missing until those operations have actually succeeded. A local run is not a cloud deployment. See `SUBMISSION.md` for task tracking.
