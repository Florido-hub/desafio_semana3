# Plano de Testes — ServeRest API

## 1. Objetivo

Validar o comportamento da API ServeRest (`https://compassuol.serverest.dev`) nos quatro domínios principais — Login, Usuários, Produtos e Carrinhos — garantindo que os contratos de resposta, os códigos HTTP, as regras de negócio e os controles de acesso estejam funcionando conforme o esperado.

---

## 2. Estratégia

| Aspecto | Decisão |
|---|---|
| Tipo de teste | Testes funcionais de API (caixa-preta) |
| Camada | Integração — chamadas HTTP diretas ao ambiente remoto |
| Ferramentas | Python 3 · pytest · requests · jsonschema |
| Abordagem | Arrange → Act → Assert: cada teste cria seus dados via fixture, executa a ação e verifica status code + corpo da resposta |
| Validação de contrato | JSON Schema aplicado nas respostas de listagem e busca por ID via `jsonschema.validate` |
| Isolamento | Fixtures com `yield` garantem criação e limpeza (teardown) automáticas por teste |
| Dados dinâmicos | Sufixo único gerado com `int(time.time()) * 100 + random.randint(1, 1000)` para evitar colisões entre execuções paralelas |
| Ambiente | Somente ambiente remoto compartilhado (sem mock, sem ambiente local) |

---

## 3. Fixtures

As fixtures seguem o padrão **create → yield → teardown**: criam o recurso via POST antes do teste, cedem os dados para o teste, e deletam via DELETE após a execução — mesmo que o teste falhe.

Todas as fixtures são registradas no `conftest.py` via `pytest_plugins`, eliminando a necessidade de imports manuais nos arquivos de teste.

| Fixture | Arquivo | Descrição |
|---|---|---|
| `usuario_existente_admin` | `fixtures/usuarios.py` | Cria e remove um usuário administrador |
| `usuario_existente_no_admin` | `fixtures/usuarios.py` | Cria e remove um usuário não-administrador |
| `auth_token` | `fixtures/auth_token.py` | Cria um usuário admin dedicado, faz login e retorna o Bearer token |
| `auth_token_no_admin` | `fixtures/auth_token.py` | Depende de `usuario_existente_no_admin` — faz login e retorna o Bearer token |
| `produto_existente` | `fixtures/produtos.py` | Depende de `auth_token` — cria e remove um produto |

### Schemas de validação

| Schema | Arquivo | Usado em |
|---|---|---|
| `USUARIO_SCHEMA` | `fixtures/utils/usuario_schema.py` | GET `/usuarios` — valida lista com `quantidade` e array de usuários |
| `USUARIO_SCHEMA_ID` | `fixtures/utils/usuario_schema.py` | GET `/usuarios/:id` — valida objeto de usuário individual |
| `PRODUTO_SCHEMA` | `fixtures/utils/produto_schema.py` | GET `/produtos` — valida lista com `quantidade` e array de produtos |
| `PRODUTO_SCHEMA_ID` | `fixtures/utils/produto_schema.py` | GET `/produtos/:id` — valida objeto de produto individual |

---

## 4. Escopo

### 4.1 Coberto

- `POST /login` — autenticação com credenciais válidas e inválidas
- `GET /usuarios` — listagem com validação de schema
- `GET /usuarios/:id` — busca por ID com validação de schema
- `POST /usuarios` — cadastro (sucesso, e-mail duplicado, campos obrigatórios via parametrize, e-mail inválido)
- `PUT /usuarios/:id` — atualização (sucesso, upsert, e-mail duplicado, campo obrigatório ausente)
- `DELETE /usuarios/:id` — remoção (sucesso e ID inexistente)
- `GET /produtos` — listagem com validação de schema
- `GET /produtos/:id` — busca por ID com validação de schema
- `POST /produtos` — cadastro (admin, não-admin, sem token, token inválido, validações de campo)
- `PUT /produtos/:id` — atualização (sucesso, upsert, sem token, não-admin, nome duplicado)
- `DELETE /produtos/:id` — remoção (sucesso, ID inexistente, sem token, não-admin)
- `POST /carrinhos` — criação de carrinho (sucesso)

### 4.2 Fora do escopo (a implementar)

- `GET /carrinhos` — não implementado ainda
- `GET /carrinhos/:id` — não implementado ainda
- `DELETE /carrinhos/concluir-compra` — não implementado ainda
- Casos de erro de `POST /carrinhos` (produto duplicado, produto inexistente, estoque insuficiente, sem autenticação, segundo carrinho)
- Testes de carga ou performance

---

## 5. Cenários por Endpoint

Legenda: ✅ Implementado · ⬜ A implementar · 🟢 Sucesso · 🔴 Erro

### 5.1 `POST /login`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| L01 | 🟢 | Login com credenciais válidas | `test_login_success` | 200 + `authorization` no body | ✅ |
| L02 | 🔴 | Login com senha incorreta | `test_login_com_senha_errada` | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L03 | 🔴 | Login com e-mail inexistente | `test_login_com_email_inexistente` | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L04 | 🔴 | Login sem o campo `email` | `test_login_com_email_ausente_no_body` | 400 + `"email não pode ficar em branco"` | ✅ |
| L05 | 🔴 | Login sem o campo `password` | `test_login_com_senha_ausente_no_body` | 400 + `"password não pode ficar em branco"` | ✅ |
| L06 | 🔴 | Login com ambos os campos vazios | `test_login_com_body_vazio` | 400 + ambas as mensagens de erro | ✅ |

### 5.2 `GET /usuarios`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U01 | 🟢 | Listar usuários com validação de schema e contagem | `test_listar_usuario` | 200 + schema válido + `quantidade == len(usuarios)` | ✅ |

### 5.3 `GET /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U02 | 🟢 | Buscar usuário por ID com validação de schema | `test_listar_usuario_pelo_id` | 200 + schema válido + `_id` correto | ✅ |
| U03 | 🔴 | Buscar usuário com ID inexistente | `test_listar_usuario_com_id_inexistente` | 400 + `"Usuário não encontrado"` | ✅ |

### 5.4 `POST /usuarios`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U04 | 🟢 | Criar usuário com dados válidos | `test_criar_usuario_success` | 201 + `_id` no body | ✅ |
| U05 | 🔴 | Criar usuário com e-mail já cadastrado | `test_criar_usuario_com_email_em_uso` | 400 + `"Este email já está sendo usado"` | ✅ |
| U06 | 🔴 | Criar usuário com cada campo obrigatório ausente | `test_criar_usuario_com_body_vazio` (parametrize) | 400 por campo | ✅ |
| U07 | 🔴 | Criar usuário com e-mail em formato inválido | `test_criar_usuario_com_email_inválido` | 400 + `"email deve ser um email válido"` | ✅ |

### 5.5 `PUT /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U08 | 🟢 | Atualizar usuário existente | `test_atualizar_usuario_success` | 200 + `"Registro alterado com sucesso"` | ✅ |
| U09 | 🟢 | Atualizar usuário inexistente (upsert) | `test_atualizar_usuario_inexistente` | 201 + `_id` no body | ✅ |
| U10 | 🔴 | Atualizar para e-mail já usado por outro usuário | `test_atualizar_usuario_com_email_em_uso` | 400 + `"Este email já está sendo usado"` | ✅ |
| U11 | 🔴 | Atualizar com campo obrigatório vazio | `test_atualizar_usuario_com_campo_obrigatorio_ausente` | 400 + `"nome não pode ficar em branco"` | ✅ |

### 5.6 `DELETE /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U12 | 🟢 | Deletar usuário existente | `test_deletar_usuario_success` | 200 + mensagem de exclusão | ✅ |
| U13 | 🟢 | Deletar usuário com ID inexistente | `test_deletar_usuario_com_id_inexistente` | 200 + `"Nenhum registro excluído"` | ✅ |

> **Obs.:** A API retorna 200 (não 404) ao deletar um ID inexistente — comportamento documentado em `test_deletar_usuario_com_id_inexistente`.

### 5.7 `GET /produtos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P01 | 🟢 | Listar produtos com validação de schema e contagem | `test_listar_produto` | 200 + schema válido + `quantidade == len(produtos)` | ✅ |
| P02 | 🟢 | Filtrar por query param `nome` | `test_listar_produto_com_parametro_nome` | 200 + lista filtrada corretamente | ✅ |

### 5.8 `GET /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P03 | 🟢 | Buscar produto por ID com validação de schema | `test_listar_produto_pelo_id` | 200 + schema válido + `_id` correto | ✅ |
| P04 | 🔴 | Buscar produto com ID inexistente | `test_listar_produto_com_id_inexistente` | 400 + `"Produto não encontrado"` | ✅ |

### 5.9 `POST /produtos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P05 | 🟢 | Criar produto como administrador | `test_criar_produto_success` | 201 + `_id` no body | ✅ |
| P06 | 🔴 | Criar produto como usuário não-admin | `test_criar_produto_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P07 | 🔴 | Criar produto sem header de autenticação | `test_criar_produto_sem_header_de_autenticacao` | 401 + mensagem de token ausente | ✅ |
| P08 | 🔴 | Criar produto com token inválido | `test_criar_produto_com_token_invalido` | 401 + mensagem de token inválido | ✅ |
| P09 | 🔴 | Criar produto com `nome` vazio | `test_criar_produto_sem_nome` | 400 + `"nome não pode ficar em branco"` | ✅ |
| P10 | 🔴 | Criar produto com `preco` vazio | `test_criar_produto_sem_preco` | 400 + `"preco deve ser um número"` | ✅ |
| P11 | 🔴 | Criar produto com `preco` negativo | `test_criar_produto_preco_negativo` | 400 + `"preco deve ser um número positivo"` | ✅ |
| P12 | 🔴 | Criar produto com `quantidade` negativa | `test_criar_produto_quantidade_negativa` | 400 + `"quantidade deve ser maior ou igual a 0"` | ✅ |

### 5.10 `PUT /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P13 | 🟢 | Atualizar produto existente como admin | `test_atualizar_produto_success` | 200 + `"Registro alterado com sucesso"` | ✅ |
| P14 | 🟢 | Atualizar produto inexistente como admin (upsert) | `test_atualizar_produto_inexistente` | 201 + `_id` no body | ✅ |
| P15 | 🔴 | Atualizar produto com token inválido | `test_atualizar_produto_sem_token` | 401 + mensagem de token inválido | ✅ |
| P16 | 🔴 | Atualizar produto como usuário não-admin | `test_atualizar_produto_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P17 | 🔴 | Atualizar produto com nome já usado por outro produto | `test_atualizar_produto_com_mesmo_nome` | 400 + `"Já existe produto com esse nome"` | ✅ |

### 5.11 `DELETE /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P18 | 🟢 | Deletar produto existente como admin | `test_deletar_produto_success` | 200 + mensagem de exclusão | ✅ |
| P19 | 🟢 | Deletar produto com ID inexistente | `test_deletar_produto_com_id_inexistente` | 200 + `"Nenhum registro excluído"` | ✅ |
| P20 | 🔴 | Deletar produto com token inválido | `test_deletar_produto_sem_autenticacao` | 401 + mensagem de token inválido | ✅ |
| P21 | 🔴 | Deletar produto como usuário não-admin | `test_deletar_produto_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |

### 5.12 `POST /carrinhos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C01 | 🟢 | Criar carrinho com produto válido | `test_criar_carrinho_success` | 201 + `_id` no body | ✅ |
| C02 | 🔴 | Criar segundo carrinho para o mesmo usuário | — | 400 + `"Não é permitido ter mais de 1 carrinho"` | ⬜ |
| C03 | 🔴 | Criar carrinho com produto inexistente | — | 400 + `"Produto não encontrado"` | ⬜ |
| C04 | 🔴 | Criar carrinho com quantidade maior que o estoque | — | 400 + `"Produto não possui quantidade suficiente"` | ⬜ |
| C05 | 🔴 | Criar carrinho sem autenticação | — | 401 + mensagem de token ausente | ⬜ |
| C06 | 🔴 | Criar carrinho com produto duplicado na lista | — | 400 + `"Não é permitido possuir produto duplicado"` | ⬜ |

### 5.13 `GET /carrinhos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C07 | 🟢 | Listar todos os carrinhos | — | 200 + lista no body | ⬜ |
| C08 | 🟢 | Filtrar carrinhos por `idUsuario` | — | 200 + lista filtrada | ⬜ |

### 5.14 `GET /carrinhos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C09 | 🟢 | Buscar carrinho por ID válido | — | 200 + `precoTotal` e `quantidadeTotal` corretos | ⬜ |
| C10 | 🔴 | Buscar carrinho com ID inexistente | — | 400 + `"Carrinho não encontrado"` | ⬜ |

### 5.15 `DELETE /carrinhos/concluir-compra`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C11 | 🟢 | Concluir compra com carrinho ativo | — | 200 + estoque decrementado | ⬜ |
| C12 | 🟢 | Concluir compra sem carrinho ativo | — | 200 + `"Não foi encontrado carrinho para esse usuário"` | ⬜ |
| C13 | 🔴 | Concluir compra sem autenticação | — | 401 + mensagem de token ausente | ⬜ |

### 5.16 `DELETE /carrinhos/cancelar-compra`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C14 | 🟢 | Cancelar compra com carrinho ativo | — | 200 + estoque restaurado | ✅ (via teardown) |
| C15 | 🟢 | Cancelar compra sem carrinho ativo | — | 200 + `"Não foi encontrado carrinho para esse usuário"` | ⬜ |
| C16 | 🔴 | Cancelar compra sem autenticação | — | 401 + mensagem de token ausente | ⬜ |

---

## 6. Critérios de Qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

1. **Isolado** — cria e remove seus próprios dados; não depende de estado pré-existente no ambiente.
2. **Determinístico** — passa e falha consistentemente nas mesmas condições; sem dependência de ordem de execução.
3. **Assertivo** — verifica status code HTTP *e* ao menos um campo relevante do corpo da resposta.
4. **Nomeado corretamente** — segue o padrão `test_<ação>_<recurso>_<condição>` em português.
5. **Sem vazamento de dados** — o teardown da fixture remove todos os recursos criados, mesmo que o teste falhe.
6. **Legível** — payload, chamada HTTP e asserções são visíveis no corpo do teste sem necessidade de abrir outros arquivos.
7. **Categorizado** — está no arquivo correto (`test_queries_` para leituras, `test_commands_` para escrita/deleção).
8. **Schema validado** — endpoints de listagem e busca por ID devem validar a estrutura da resposta via JSON Schema.

---

## 7. Melhorias Futuras

| Item | Descrição |
|---|---|
| Carrinhos — queries | Implementar `test_queries_carrinhos.py` (arquivo existe mas está vazio) |
| Carrinhos — casos de erro | Implementar os cenários C02–C06 e C10–C13, C15–C16 |
| Schema de carrinhos | Criar `carrinho_schema.py` em `fixtures/utils/` para validar respostas de GET /carrinhos |
| `auth_token` sem teardown | A fixture `auth_token` cria um usuário mas não o remove no teardown — pode acumular dados no servidor |
