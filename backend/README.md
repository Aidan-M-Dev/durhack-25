# Backend (Flask) README

This folder contains a minimal Flask app configured to talk to Supabase.

Quick start (local):

1. Create and activate a virtualenv:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables and set your Supabase values:

```bash
cp .env.example .env
# Edit .env and set SUPABASE_URL and SUPABASE_KEY
```

4. Run the app:

```bash
python app.py
```

Endpoints:
- GET /api/hello — simple health/hello endpoint
- GET /api/user — requires Authorization: Bearer <access_token>; returns user info from Supabase (placeholder — adjust for your supabase client version)

Notes:
- The Supabase Python client API may change between versions. If user lookups fail, refer to your installed `supabase` package docs and update `app.py` accordingly.
