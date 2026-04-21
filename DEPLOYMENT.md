# Deployment Guide

This backend is configured for Render plus PostgreSQL.

## Render Blueprint

1. Push this repository to GitHub.
2. In Render, create a new Blueprint from this repository.
3. Render will read `render.yaml`, create the PostgreSQL database, install dependencies, collect static files, run migrations on startup, and start Gunicorn.
4. After the first deploy, copy the backend service URL.
5. Update these Render environment variables if your generated service name differs:

```text
ALLOWED_HOSTS=<your-render-host>
CORS_ALLOWED_ORIGINS=<your-vercel-frontend-url>
CSRF_TRUSTED_ORIGINS=<your-vercel-frontend-url>
```

## Manual Render Setup

Use these commands if you create the service manually:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
python manage.py migrate && gunicorn config.wsgi:application
```

Required production variables:

```text
SECRET_KEY=<generated-secret>
DEBUG=False
ALLOWED_HOSTS=<your-render-host>
CORS_ALLOWED_ORIGINS=<your-frontend-origin>
CSRF_TRUSTED_ORIGINS=<your-frontend-origin>
DATABASE_URL=<render-postgres-connection-string>
DB_SSL_REQUIRE=True
CELERY_TASK_ALWAYS_EAGER=True
```

## Smoke Test

After deployment:

```bash
curl https://<your-render-host>/api/docs/
```

Then create a user through the frontend or with `POST /api/auth/register/`.
