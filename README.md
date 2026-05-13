# 📝 Task Manager API

A small full-stack task manager built around a **FastAPI + SQLAlchemy** REST API and a vanilla-JS frontend. Demonstrates clean CRUD, Pydantic validation, schema separation (input vs. response), CORS-aware deployment, and CI on every push.

![CI](https://github.com/EriktheRed95/task-manager-api/actions/workflows/ci.yml/badge.svg)

## Features

- Create, read, update, and delete tasks
- Filter tasks by title substring
- Persistent SQLite via SQLAlchemy (in-memory for tests)
- Pydantic v2 input/response separation — responses include the auto-generated `id`
- CORS middleware so the frontend can call the API across origins
- Vanilla-JS frontend with XSS-safe DOM rendering (no `innerHTML` interpolation)
- 7 pytest integration tests, GitHub Actions CI

## Tech stack

`Python 3.11` · `FastAPI` · `SQLAlchemy 2.0` · `Pydantic v2` · `SQLite` · `pytest` · `httpx`

## Run locally

```bash
git clone https://github.com/EriktheRed95/task-manager-api.git
cd task-manager-api/backend

python -m venv ../venv
# Windows:  ..\venv\Scripts\activate
# macOS/Linux: source ../venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The API is now at `http://127.0.0.1:8000` and the auto-generated docs at `http://127.0.0.1:8000/docs`.

For the frontend, just open `frontend/index.html` in a browser — it talks to the backend at `127.0.0.1:8000` by default.

## Run the tests

```bash
cd backend
pytest -v
```

## Deploy

**Backend (Render.com):** the included [`render.yaml`](render.yaml) is a one-click blueprint.
1. Push this repo to GitHub.
2. Create a new "Blueprint" service at [render.com/dashboard](https://dashboard.render.com).
3. Point it at this repo. Render reads `render.yaml` and provisions a free-tier web service.

**Frontend (Netlify):** the included [`netlify.toml`](netlify.toml) publishes `frontend/` as a static site.
1. Connect this repo on [app.netlify.com](https://app.netlify.com).
2. Update `API_URL` in `frontend/index.html` from `http://127.0.0.1:8000/tasks` to your Render URL.

## API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tasks` | Create a task |
| `GET`  | `/tasks` | List all tasks (optional `?title=…` filter) |
| `GET`  | `/tasks/{id}` | Get one task |
| `PUT`  | `/tasks/{id}` | Replace a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
