# Tech Stack

## Language & Runtime
- **Python 3** (virtual environment in `.venv/`)

## Testing Framework
- **pytest** — test discovery, fixtures, and assertions
- **requests** — HTTP client for all API calls (no special REST library)

## Key Libraries
- `pytest` — core test runner and fixture system
- `requests` — all HTTP requests (GET, POST, PUT, DELETE)
- `time` — used to generate unique names/emails via `int(time.time())` or `int(time.time()*100)`

## Configuration
- Base URL is defined in `tests/config/settings.py` as `ENDPOINT`
- No `.env` file — configuration is hardcoded in settings

## Common Commands

```bash
# Run all tests
pytest

# Run a specific module
pytest tests/usuarios/

# Run a specific test file
pytest tests/produtos/test_commands_produto.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

> Tests make real HTTP calls to the remote ServeRest instance. An internet connection is required.
