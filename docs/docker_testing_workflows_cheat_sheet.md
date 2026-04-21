# Docker Testing and Development Workflows Cheat Sheet

This document provides a single consolidated reference for running your **pcc-learning-log** application and test suites using Docker. These are the practical commands you'll use daily during development and automation work.

---

# Start Application Container

Use this at the beginning of your work session.

```bash
docker compose up
```

Run in background (optional):

```bash
docker compose up -d
```

Stop the container:

```bash
Ctrl + C
```

Or:

```bash
docker compose down
```

---

# Run All Pytest Test Cases

Use for unit tests, view tests, API tests, and regression suites.

```bash
docker compose exec web pytest
```

Recommended verbose output:

```bash
docker compose exec web pytest -v
```

---

# Run Specific Test File

```bash
docker compose exec web pytest tests/test_views.py
```

---

# Run Specific Test Case

```bash
docker compose exec web pytest tests/test_views.py::test_login
```

---

# Run Playwright End-to-End Tests

Start the Dockerized application first:

```bash
docker compose up
```

Then run Playwright tests from your automation framework:

```bash
pytest tests/e2e
```

Or using markers:

```bash
pytest -m e2e
```

Application base URL:

```python
BASE_URL = "http://localhost:8000"
```

---

# Run Django Management Commands Inside Docker

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Open Django shell:

```bash
docker compose exec web python manage.py shell
```

Collect static files (future production use):

```bash
docker compose exec web python manage.py collectstatic
```

---

# Rebuild Image After Dependency Changes

Use this when you change:

- requirements.txt
- Dockerfile
- Python version
- System dependencies

```bash
docker compose build
docker compose up
```

---

# Restart Container After Code Changes

Use this when you change application code.

```bash
docker compose up
```

Most code changes do NOT require rebuilding the image.

---

# Run Tests in Clean Environment (CI Simulation)

Use when validating deterministic test runs.

```bash
docker compose down
docker compose build
docker compose up -d
docker compose exec web pytest
```

---

# Full Environment Reset

Use when database or container state becomes inconsistent.

```bash
docker compose down -v
docker compose build
docker compose up
```

---

# View Running Containers

```bash
docker ps
```

---

# View Container Logs

```bash
docker compose logs
```

---

# Daily Development Workflow (Typical)

```bash
docker compose up
docker compose exec web pytest
```

---

# Key Decision Rule

```
Changed code?           → docker compose up
Changed dependencies?   → docker compose build
Need clean test run?    → docker compose down && build
```

