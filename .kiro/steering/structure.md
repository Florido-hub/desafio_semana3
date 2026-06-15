# Project Structure

```
tests/
├── config/
│   └── settings.py          # Global config (ENDPOINT base URL)
├── fixtures/
│   ├── auth_token.py         # auth_token fixture — logs in and returns Bearer token
│   ├── usuario.py            # usuario_existente_admin / usuario_existente_no_admin fixtures
│   └── products.py           # produto_existente fixture (depends on auth_token)
├── login/
│   └── test_login.py
├── usuarios/
│   ├── test_queries_usuario.py   # GET /usuarios
│   └── test_commands_usuario.py  # POST, DELETE /usuarios
├── produtos/
│   ├── test_queries_produto.py   # GET /produtos
│   └── test_commands_produto.py  # POST, PUT, DELETE /produtos
└── carrinhos/
    ├── test_queries_carrinhos.py  # GET /carrinhos (empty)
    └── test_commands_carrinhos.py # POST, DELETE /carrinhos (empty)
```

## Conventions

### File naming
- Test files: `test_queries_<resource>.py` for read operations, `test_commands_<resource>.py` for write operations
- One folder per API resource under `tests/`

### Fixtures
- All reusable fixtures live in `tests/fixtures/` and are imported explicitly into test files with `from tests.fixtures.<module> import *`
- Fixtures follow a **create → yield → teardown** pattern: the resource is created via POST before the test, yielded for use, then deleted via DELETE after
- Use `int(time.time())` or `int(time.time()*100)` to generate unique values for names and emails, avoiding conflicts between test runs

### Imports
- Always import `ENDPOINT` from `tests.config.settings`
- Fixture modules are imported with wildcard (`import *`) so pytest can discover them

### Test naming
- Snake case: `test_<action>_<resource>_<condition>` (e.g. `test_create_user_email_already_registered`)
- Names are in English even though variable/payload content is in Portuguese

### Authentication
- Authenticated endpoints require an `Authorization` header with the token from the `auth_token` fixture
- Only admin users can create/update/delete products; tests for non-admin access assert `403`

### Assertions
- Always assert `response.status_code` first
- Then assert relevant fields in `response.json()`
- Response messages from the API are in Portuguese (e.g. `"Cadastro realizado com sucesso"`)
