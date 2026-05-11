content = """# Muzukuru API - Backend

Flask REST API for the full-stack To-Do application with user management, authentication, and API docs.

## Tech Stack

- **Framework:** Flask 3.1.3 | **ORM:** SQLAlchemy 2.0+ | **API:** flask-smorest 0.47.0
- **Database:** SQLite (dev) | **Migrations:** Alembic | **Validation:** Marshmallow 4.3.0

## Quick Start

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
flask db upgrade
flask run
```

API: `http://127.0.0.1:5000`
Docs: `http://127.0.0.1:5000/docs`

## API Endpoints

### Health & Docs
- `GET /health` — Health check
- `GET /docs` — Swagger UI
- `GET /openapi.json` — OpenAPI 3.0.2 spec

### Users (Current)
- `GET /api/users` — List all
- `POST /api/users` — Create
- `GET /api/users/{id}` — Get by ID
- `PUT /api/users/{id}` — Update
- `DELETE /api/users/{id}` — Delete

### Authentication (TODO)
- `POST /register` — Create account (password hashing)
- `POST /login` — Authenticate (JWT token)
- `GET /protected` — Verify Bearer token

## Project Structure

```
app/
├── __init__.py           # App factory
├── config/config.py      # Config (Dev, Test, Prod)
├── db/
│   ├── __init__.py       # SQLAlchemy instance
│   └── models.py         # User model
├── modules/
│   ├── errors/           # Error handlers (400, 404, 422, 500, etc.)
│   ├── health/           # /health, /docs, /openapi.json
│   └── users/            # CRUD routes
└── templates/swagger_ui.html
```

## Configuration

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY=your-secret-key
```

## Database Commands

```bash
flask db migrate -m "description"  # Generate migration
flask db upgrade                   # Apply migration
flask db downgrade                 # Rollback
```

## TODO (Remaining)

- [ ] Authentication: password hashing, JWT, `/register`, `/login`, `/protected`
- [ ] Logging: request/error logs to `app.log`
- [ ] CORS: enable for `localhost:3000`
- [ ] Testing: pytest suite
- [ ] Deployment: PostgreSQL, Docker, gunicorn
"""

with open("README.md", "w") as f:
    f.write(content)

print("README.md updated!")
