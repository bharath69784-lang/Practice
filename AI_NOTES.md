# AI Notes

> **Before submitting:** this is a draft. Fill in the bracketed parts
> with what you actually did after reading through the code and running
> it yourself — see the message accompanying this file for why that
> matters.

## What was AI-generated vs. written by me

- I used Claude to generate the initial implementation: `src/app.py`
  (Flask routes), `src/storage.py` (in-memory store), `src/validators.py`
  (request validation), and the pytest suite in `tests/test_api.py`.
- [Describe what you changed, added, or rewrote yourself — e.g. did you
  rename anything, change the route design, add an endpoint, adjust
  validation rules, restructure the tests?]

## What I validated, tested, or changed, and why

- I ran `pytest tests/ -v` on a clean checkout and confirmed all
  [N] tests pass. [Replace with your actual result.]
- I started the server locally and manually exercised the endpoints
  with `curl` (add, list, filter by category, total, summary, delete)
  to confirm the behavior matched the README. [Confirm this yourself —
  don't just take my word for it.]
- [Note anything you specifically checked or changed, e.g.: "I checked
  that amount=0 is rejected", "I changed date validation to also allow
  ISO datetimes", "I reviewed the UUID-based ID scheme and decided to
  keep it because sequential IDs would leak the count of expenses",
  etc.]

## AI suggestions I didn't use, and why

- [If you asked Claude for the optional bonus feature (search, monthly
  summary, Swagger docs, Docker) or any alternative design and decided
  against it, note that here and why.]
- [If nothing applies, say so honestly rather than leaving this blank.]
