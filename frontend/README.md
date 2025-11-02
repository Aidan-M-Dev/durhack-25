# Frontend (Vue + Vite + Tailwind)

This is a minimal Vue 3 + Vite frontend wired to call the Flask backend at /api.

Quick start:

1. Install node dependencies:

```bash
cd frontend
npm install
```


2. Create a `.env` file.

You can either put a `.env` inside `frontend/` or (recommended) use a single shared `.env` at the repository root. This scaffold now prefers a repository-root `.env` so both frontend and backend use the same values.

Example shared (repository root `.env`) — recommended:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-or-anon-key
```

Important: do NOT add client-exposed `VITE_` keys here for any secret values. If you do, they will be visible in the browser. Instead:

- Keep only server-side Supabase keys (like service-role or restricted keys) in the repo-root `.env`.
- Implement auth and privileged Supabase operations via the backend API. The backend uses `SUPABASE_KEY` to call Supabase securely and can set an HttpOnly cookie or session for the browser.

If you prefer a per-folder `.env` for non-sensitive, client-safe values, create `frontend/.env` and only include variables prefixed with `VITE_` that are safe to expose.

3. Run dev server:

```bash
npm run dev
```

Notes:
- Vite will proxy unknown requests to the backend only if you configure a proxy. For local development you can run the Flask backend on port 5000 and configure a proxy in `vite.config.js` or call the backend via absolute URL (http://localhost:5000/api/...).
 - The frontend should not include a Supabase client if you don't want any Supabase keys exposed. Instead, call backend auth endpoints (e.g. `/api/auth/signup`, `/api/auth/signin`) and let the backend handle Supabase operations.
