# Docker Setup Guide

This guide explains how to run the Module Guide application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Setup Instructions

### 1. Configure Environment Variables (Optional)

The application uses sensible defaults for development. You can optionally copy and customize the environment file:

```bash
cp .env.example .env
```

The database connection is automatically configured by docker-compose. No additional configuration needed!

### 2. Build and Run with Docker Compose

Build and start all services:

```bash
docker-compose up --build
```

Or run in detached mode (background):

```bash
docker-compose up -d --build
```

### 3. Access the Application

Once the containers are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

### 4. Database Initialization

The PostgreSQL database is automatically initialized with:
- Schema (tables and relationships)
- Stored functions for querying lecturers and courses
- Test data with sample modules, reviews, and users

All SQL scripts in `backend/sql_statements/` are executed automatically on first startup.

### 5. Stop the Application

```bash
docker-compose down
```

To stop and remove all volumes:

```bash
docker-compose down -v
```

## Development with Docker

The Docker setup includes volume mounting for hot-reload during development:

- Changes to backend Python files will automatically reload the Flask server
- Changes to frontend Vue files will trigger Vite's hot module replacement

## Viewing Logs

View logs for all services:

```bash
docker-compose logs -f
```

View logs for a specific service:

```bash
docker-compose logs -f frontend
docker-compose logs -f backend
```

## Troubleshooting

### Port Already in Use

If ports 5000 or 5173 are already in use, you can modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "3000:5000"  # Use port 3000 on host instead of 5000
```

### Backend Connection Issues

If the frontend can't connect to the backend:
1. Check that both containers are running: `docker-compose ps`
2. Check the backend logs: `docker-compose logs backend`
3. Verify your `.env` file has correct Supabase credentials

### Rebuilding After Changes

If you modify `package.json`, `requirements.txt`, or Dockerfiles:

```bash
docker-compose down
docker-compose up --build
```

## Production Build

For production, you would typically:

1. Build the frontend for production:
   ```bash
   cd frontend
   npm run build
   ```

2. Serve the built files with a production server (nginx, etc.)

3. Run the backend with a production WSGI server (gunicorn, etc.)

This Docker setup is optimized for development. For production deployment, additional configuration would be needed.
