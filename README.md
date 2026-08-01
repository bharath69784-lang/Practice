# Smart Expense Tracker API

A small REST API for tracking personal expenses: add, list, filter by
category, view totals, and delete. Built with Flask, data kept in memory
(no database, resets on restart).

## Requirements
- Python 3.10+

## Install

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```bash
python -m src.app
```

The API is served at `http://localhost:5000`.

## Run the tests

```bash
pytest tests/ -v
```

## Endpoints

| Method | Path                          | Description                                  |
|--------|-------------------------------|-----------------------------------------------|
| GET    | `/`                           | Health check                                  |
| POST   | `/expenses`                   | Add an expense                                |
| GET    | `/expenses`                   | List all expenses (optional `?category=`)     |
| GET    | `/expenses/<id>`              | Get one expense                               |
| DELETE | `/expenses/<id>`              | Delete an expense                             |
| GET    | `/expenses/total`             | Overall total (optional `?category=`)         |
| GET    | `/expenses/summary`           | Overall total + breakdown by category         |

### Add an expense

```bash
curl -X POST http://localhost:5000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-30"}'
```

Required fields: `title` (non-empty string), `amount` (number > 0),
`category` (non-empty string), `date` (`YYYY-MM-DD`). The server assigns
the `id`.

### Filter by category

```bash
curl "http://localhost:5000/expenses?category=Food"
```

### Totals

```bash
curl http://localhost:5000/expenses/total              # overall
curl "http://localhost:5000/expenses/total?category=Food"  # by category
curl http://localhost:5000/expenses/summary             # both at once
```

### Delete

```bash
curl -X DELETE http://localhost:5000/expenses/<id>
```

## Project structure

```
your-repo/
  README.md
  AI_NOTES.md
  src/
    app.py          # Flask app + routes
    storage.py       # in-memory data store
    validators.py     # request validation
  tests/
    test_api.py      # pytest suite (17 tests)
```

## Design notes
- IDs are server-generated UUIDs, not client-supplied, to avoid
  collisions and keep the API in charge of identity.
- Category matching is case-insensitive on filter/total endpoints
  (`Food` and `food` are treated the same) since users will type
  categories inconsistently.
- Validation lives in its own module so it can be unit-tested
  independently of Flask routing if needed.
