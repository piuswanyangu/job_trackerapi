# Job Tracker API

A Django REST Framework API for tracking job applications, managing application statuses, and generating job-search analytics for the Job Tracker frontend.

## Problem It Solves

Job seekers often manage applications across spreadsheets, notes, and email threads. This API centralizes application data, authenticates users with JWT, protects each user's records, and exposes analytics that help users understand their job-search pipeline.

## Features

- Email-based user registration and JWT login
- Authenticated profile endpoint
- Create, read, update, and delete job applications
- Per-user application isolation
- Application statuses: applied, interview, offer, rejected
- Analytics totals by status
- OpenAPI schema and Swagger documentation
- Environment-based configuration for local and deployed environments
- Local-safe cache and Celery defaults
- API tests for authentication, CRUD, permissions, and analytics

## Tech Stack

- Python 3.11+
- Django 5
- Django REST Framework
- Simple JWT
- drf-spectacular
- django-cors-headers
- Celery with Redis support for production workers
- SQLite for local development
- Gunicorn for deployment

## Installation

```bash
git clone https://github.com/piuswanyangu/job-trackerapi.git
cd job-trackerapi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
```

On macOS or Linux, activate the virtual environment with:

```bash
source venv/bin/activate
```

## Environment Variables

Create `.env` from `.env.example`.

| Variable | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | Use `True` locally and `False` in production |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames |
| `CORS_ALLOWED_ORIGINS` | No | Comma-separated frontend origins |
| `DATABASE_URL` | No | Reserved for production database configuration |
| `CELERY_BROKER_URL` | No | Redis broker URL for deployed Celery workers |
| `CELERY_RESULT_BACKEND` | No | Celery result backend |
| `CELERY_TASK_ALWAYS_EAGER` | No | Run Celery tasks synchronously in local development |

## Run Locally

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/api/docs/
```

## API Endpoints

### Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Get JWT access and refresh tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `GET` | `/api/auth/me/` | Get authenticated user profile |

### Applications

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/applications/applications/` | List current user's applications |
| `POST` | `/api/applications/applications/` | Create application |
| `GET` | `/api/applications/applications/{id}/` | Get application detail |
| `PATCH` | `/api/applications/applications/{id}/` | Update application |
| `DELETE` | `/api/applications/applications/{id}/` | Delete application |

### Analytics

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/applications/analytics/` | Get status counts and totals |

## Example Application Payload

```json
{
  "company_name": "Acme",
  "job_title": "Frontend Engineer",
  "status": "applied"
}
```

## Folder Structure

```text
apps/
  accounts/       User model, registration, JWT profile endpoints
  applications/   Job application CRUD, analytics, signals, tests
  core/           Shared middleware and background task helpers
config/           Django settings, URLs, Celery setup
manage.py         Django command entry point
requirements.txt  Python dependencies
```

## Testing

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Deployment

This repository includes `render.yaml`, `Procfile`, `runtime.txt`, and `DEPLOYMENT.md` for Render deployment.

1. Set `DEBUG=False`.
2. Set a strong `SECRET_KEY`.
3. Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS`.
4. Set `DATABASE_URL` to a production PostgreSQL database.
5. Run migrations during deployment.
6. Run `python manage.py collectstatic --noinput`.
7. Start the app with Gunicorn:

```bash
gunicorn config.wsgi:application
```

For production Celery workers, set `CELERY_TASK_ALWAYS_EAGER=False` and provide Redis-backed `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`.

## Screenshots

Screenshots are not included because this repository is the backend API. Add screenshots of Swagger docs or API client examples if needed.

## Future Improvements

- Add PostgreSQL production settings
- Add filtering and search by company, title, and status
- Add due dates and follow-up reminders
- Add pagination metadata to frontend-facing list responses
- Add CI for tests and migration checks
- Add rate limiting for auth endpoints

## Author

Built by [Pius Wanyangu](https://github.com/piuswanyangu).
