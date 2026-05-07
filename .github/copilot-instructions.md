# GitHub Copilot Workspace Instructions

## Project Overview

**Mergington High School Activities API** - A FastAPI web application for student activities management.

- **Type**: Full-stack web application (educational)
- **Backend**: Python 3 with FastAPI and Uvicorn
- **Frontend**: HTML, CSS, JavaScript with vanilla JS (no frameworks)
- **Data**: In-memory storage (resets on server restart)
- **Deployment**: Dev container environment

## Quick Start

### Development Server

```bash
# Option 1: Run directly
python src/app.py

# Option 2: Use VS Code debugger (recommended)
# Press F5 or select "Launch Mergington WebApp" from debug menu
```

**Server runs at**: `http://localhost:8000`
- API docs: `http://localhost:8000/docs` (Swagger UI)
- Web UI: `http://localhost:8000/static/` (redirects from root)

### Auto-Reload Features

- **Backend**: Python files in `src/` reload automatically via Uvicorn
- **Frontend**: Static files in `src/static/` reload automatically
- No manual restart needed during development

## Architecture

### Backend Structure

**[src/app.py](src/app.py)** - FastAPI application
- In-memory `activities` dict: Maps activity names → details (description, schedule, max_participants, participants list)
- **GET /activities** - Returns all activities as JSON
- **POST /activities/{name}/signup** - Adds email to activity participant list
- **DELETE /activities/{name}/signup** - Removes email from activity

### Frontend Structure

**[src/static/index.html](src/static/index.html)** - Main page
- Activity cards display (generated dynamically)
- Signup form
- Message display area

**[src/static/app.js](src/static/app.js)** - Client logic
- `fetchActivities()` - Fetches and renders activity list
- `unregister()` - Removes participant from activity
- Form submission handler for signups

**[src/static/styles.css](src/static/styles.css)** - Styling

## Data Model

### Activity Object (in-memory)
```python
{
    "description": str,
    "schedule": str,
    "max_participants": int,
    "participants": list[str]  # Email addresses
}
```

### Signup Flow
1. User selects activity from dropdown
2. Enters email address
3. Frontend POSTs to `/activities/{name}/signup?email={email}`
4. Backend validates (checks availability) and adds participant
5. Frontend refreshes activity list

## Common Development Tasks

### Adding a New Activity

Edit [src/app.py](src/app.py) `activities` dict and add a new entry with the required fields (description, schedule, max_participants).

### Styling Changes

Modify [src/static/styles.css](src/static/styles.css) - changes auto-reload in browser when page refreshes.

### Frontend Logic Changes

Edit [src/static/app.js](src/static/app.js) - consider these patterns:
- Async API calls use `fetch()` with error handling
- DOM updates done via `innerHTML` (simple approach)
- Event delegation for dynamic elements (.delete-btn listeners)

### API Changes

Edit [src/app.py](src/app.py) and restart server. API docs auto-update at `/docs`.

## Testing

```bash
# Install test dependencies (already in requirements.txt)
pytest

# Watch mode (with watchfiles installed)
pytest --tb=short
```

Check [pytest.ini](pytest.ini) for configuration.

## Dependencies

See [requirements.txt](requirements.txt):
- **fastapi** - Web framework
- **uvicorn** - ASGI server with auto-reload
- **httpx** - HTTP client (mostly for testing)
- **watchfiles** - File watching for auto-reload

## Conventions

### Code Style
- Python: Follow PEP 8 (inferred by Pylance)
- JavaScript: ES6+ features, async/await pattern
- Variable naming: snake_case (Python), camelCase (JavaScript)

### Error Handling
- Backend: Raises `HTTPException` with detail messages
- Frontend: Shows alerts and logs errors to console
- Messages auto-hide after 5 seconds

### API Query Parameters
- Email parameter uses `encodeURIComponent()` for safe URLs
- Activity names also URL-encoded

## Common Pitfalls

1. **Data Loss on Restart** - All participant data stored in-memory resets when server restarts (by design for this exercise)
2. **Static Files Not Loading** - Make sure server is running; check console for 404 errors
3. **Auto-reload Not Working** - Uvicorn might have crashed; check debug console output
4. **CORS Issues** - Frontend and backend are on same origin, no CORS config needed

## Exercise Workflow

This workspace is set up for the "Getting Started with GitHub Copilot" exercise. Use this setup to:

1. Follow GitHub issue guidance in [repo's issue #1](https://github.com/drakonjatko/skills-getting-started-with-github-copilot/issues/1)
2. Test changes via the running dev server
3. Ask Copilot for help implementing features or fixing bugs
4. Use `/docs` endpoint for API exploration
5. Commit and push changes to your accelerate-with-copilot branch

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Uvicorn Documentation](https://www.uvicorn.org)
- Swagger UI (auto-generated): http://localhost:8000/docs
