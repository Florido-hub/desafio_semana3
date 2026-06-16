# Suite de Testes da API ServeRest

Este repositório contém a suite de testes automatizados desenvolvida como entrega do **Desafio Técnico da Sprint 2** do programa **AI Driven Quality Engineering**, promovido pela **AIR Academy**.

---

## Contexto

O desafio consiste em evoluir uma suite de testes de API para uma versão mais completa e profissional, cobrindo planejamento, implementação e medição de cobertura.

### API sob teste: ServeRest

A [ServeRest](https://compassuol.serverest.dev) é uma API REST pública que simula um e-commerce básico, utilizada para fins de treinamento em QA. Ela expõe quatro domínios:

| Domínio | Endpoints |
|---|---|
| Login | `POST /login` |
| Usuários | `GET/POST /usuarios`, `GET/PUT/DELETE /usuarios/:id` |
| Produtos | `GET/POST /produtos`, `GET/PUT/DELETE /produtos/:id` |
| Carrinhos | `GET/POST /carrinhos`, `GET /carrinhos/:id`, `DELETE /carrinhos/concluir-compra`, `DELETE /carrinhos/cancelar-compra` |

> Os testes fazem chamadas HTTP reais ao ambiente remoto. É necessária conexão com a internet.

---

## Objetivo da suite

Validar o comportamento da API ServeRest nos quatro domínios — garantindo que os contratos de resposta, os códigos HTTP, as regras de negócio e os controles de acesso (autenticação e autorização por perfil admin) funcionem conforme o esperado.

---

## Tecnologias

| Ferramenta | Uso |
|---|---|
| Python 3 | Linguagem principal |
| pytest | Framework de testes, fixtures e parametrize |
| requests | Cliente HTTP para todas as chamadas à API |
| jsonschema | Validação da estrutura das respostas (Extra 1) |

---

## Pré-requisitos

- Python 3.8+
- Ambiente virtual ativo (`.venv/`)
- Conexão com a internet

---

## Instalação

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

---

## Como executar

```bash
# Executar todos os testes
pytest

# Executar um domínio específico
pytest tests/usuarios/
pytest tests/produtos/
pytest tests/login/
pytest tests/carrinhos/

# Executar um marcador específico
pytest create
pytest create_user
pytest update_product
pytest login

# Executar com saída detalhada
pytest -v 

# Parar na primeira falha
pytest -x
```

---

## Estrutura do projeto

```
tests/
├── conftest.py                        # Registro central de fixtures via pytest_plugins
├── config/
│   └── constants.py                   # ENDPOINT base da API
├── fixtures/
│   ├── usuarios.py                    # usuario_existente_admin / usuario_existente_no_admin
│   ├── auth_token.py                  # auth_token (admin) / auth_token_no_admin
│   ├── produtos.py                    # produto_existente
│   └── utils/
│       ├── usuario_schema.py          # USUARIO_SCHEMA / USUARIO_SCHEMA_ID
│       └── produto_schema.py          # PRODUTO_SCHEMA / PRODUTO_SCHEMA_ID
├── login/
│   └── test_login.py
├── usuarios/
│   ├── test_queries_usuario.py        # GET /usuarios
│   └── test_commands_usuario.py       # POST, PUT, DELETE /usuarios
├── produtos/
│   ├── test_queries_produto.py        # GET /produtos
│   └── test_commands_produto.py       # POST, PUT, DELETE /produtos
└── carrinhos/
    ├── test_queries_carrinhos.py       # GET /carrinhos (a implementar)
    └── test_commands_carrinhos.py      # POST /carrinhos
```

### Fixtures

As fixtures seguem o padrão **create → yield → teardown** e são registradas centralmente no `conftest.py`, sem necessidade de imports manuais nos arquivos de teste.

| Fixture | Descrição |
|---|---|
| `usuario_existente_admin` | Cria e remove um usuário administrador com sufixo único |
| `usuario_existente_no_admin` | Cria e remove um usuário não-administrador com sufixo único |
| `auth_token` | Cria um usuário admin dedicado, faz login e retorna o Bearer token |
| `auth_token_no_admin` | Depende de `usuario_existente_no_admin` — faz login e retorna o Bearer token |
| `produto_existente` | Depende de `auth_token` — cria e remove um produto |

### Validação de Schema (Extra 1)

Schemas JSON definidos em `fixtures/utils/` e aplicados nos testes de GET via `jsonschema.validate`:

| Schema | Endpoint validado |
|---|---|
| `USUARIO_SCHEMA` | GET `/usuarios` — valida lista com `quantidade` e array de usuários |
| `USUARIO_SCHEMA_ID` | GET `/usuarios/:id` — valida objeto de usuário individual |
| `PRODUTO_SCHEMA` | GET `/produtos` — valida lista com `quantidade` e array de produtos |
| `PRODUTO_SCHEMA_ID` | GET `/produtos/:id` — valida objeto de produto individual |

---

## Cobertura de Testes

### Método utilizado: Operator Coverage

A cobertura foi calculada pelo critério de **Operator Coverage**, conforme o artigo [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b).

Esse critério mede quantas operações da API (combinação de **endpoint + método HTTP**) estão cobertas pela suite. A fórmula aplicada é:

```
Cobertura = (Operações cobertas / Total de operações da API) × 100
```

### Resultado

| Operação | Coberta |
|---|---|
| POST `/login` | ✅ |
| GET `/usuarios` | ✅ |
| GET `/usuarios/:id` | ✅ |
| POST `/usuarios` | ✅ |
| PUT `/usuarios/:id` | ✅ |
| DELETE `/usuarios/:id` | ✅ |
| GET `/produtos` | ✅ |
| GET `/produtos/:id` | ✅ |
| POST `/produtos` | ✅ |
| PUT `/produtos/:id` | ✅ |
| DELETE `/produtos/:id` | ✅ |
| POST `/carrinhos` | ✅ |
| GET `/carrinhos` | ❌ |
| GET `/carrinhos/:id` | ❌ |
| DELETE `/carrinhos/concluir-compra` | ❌ |
| DELETE `/carrinhos/cancelar-compra` | ✅ (via teardown) |
| **Total** | **13 / 16** |

> **Cobertura total atingida: 81%**

### Operações fora da cobertura e justificativa

| Operação | Motivo |
|---|---|
| GET `/carrinhos` | `test_queries_carrinhos.py` existe mas está vazio — a implementar |
| GET `/carrinhos/:id` | `test_queries_carrinhos.py` existe mas está vazio — a implementar |
| DELETE `/carrinhos/concluir-compra` | Módulo de carrinhos em desenvolvimento |

Os domínios **Login**, **Usuários** e **Produtos** atingiram **100% de cobertura** pelo critério Operator Coverage.

---

## Bug Report

Bugs encontrados durante a execução dos testes estão reportados na aba [Issues](../../issues) do repositório, seguindo o padrão: passos para reproduzir, comportamento esperado, comportamento obtido, severidade e evidências.

---

## Plano de Testes

Consulte o [PLANO-DE-TESTES.md](./PLANO-DE-TESTES.md) para a descrição completa de todos os cenários mapeados, estratégia, escopo e critérios de qualidade.
