# Plano de Testes — ServeRest API

## 1. Objetivo

Validar o comportamento da API ServeRest (`https://compassuol.serverest.dev`) nos quatro domínios principais — Login, Usuários, Produtos e Carrinhos — garantindo que os contratos de resposta, os códigos HTTP, as regras de negócio e os controles de acesso estejam funcionando conforme o esperado.

---

## 2. Estratégia

| Aspecto | Decisão |
|---|---|
| Tipo de teste | Testes funcionais de API (caixa-preta) |
| Camada | Integração — chamadas HTTP diretas ao ambiente remoto |
| Ferramentas | Python 3 · pytest · requests |
| Abordagem | Arrange → Act → Assert: cada teste cria seus dados via fixture, executa a ação e verifica status code + corpo da resposta |
| Isolamento | Fixtures com `yield` garantem criação e limpeza (teardown) automáticas por teste |
| Dados dinâmicos | Nomes e e-mails únicos gerados com `int(time.time())` ou `int(time.time()*100)` para evitar colisões entre execuções |
| Ambiente | Somente ambiente remoto compartilhado (sem mock, sem ambiente local) |

---

## 3. Fixtures

| Fixture | Arquivo | Descrição |
|---|---|---|
| `usuario_existente_admin` | `fixtures/usuario.py` | Cria usuário admin via POST, yield com dados, DELETE no teardown |
| `usuario_existente_no_admin` | `fixtures/usuario.py` | Cria usuário não-admin via POST, yield com dados, DELETE no teardown |
| `auth_token` | `fixtures/auth_token.py` | Depende de `usuario_existente_admin`; faz login e retorna o Bearer token |
| `auth_token_no_admin` | `fixtures/auth_token.py` | Depende de `usuario_existente_no_admin`; faz login e retorna o Bearer token |
| `produto_existente` | `fixtures/products.py` | Depende de `auth_token`; cria produto via POST, yield com dados, DELETE no teardown |

---

## 4. Escopo

### 4.1 Coberto

- `POST /login` — autenticação com credenciais válidas e inválidas
- `GET /usuarios` — listagem
- `GET /usuarios/:id` — busca por ID (sucesso e ID inexistente)
- `POST /usuarios` — cadastro (sucesso, e-mail duplicado, body vazio, e-mail inválido)
- `PUT /usuarios/:id` — atualização (sucesso, upsert, e-mail duplicado, campo obrigatório ausente)
- `DELETE /usuarios/:id` — remoção (sucesso e ID inexistente)
- `GET /produtos` — listagem e filtro por `nome`
- `GET /produtos/:id` — busca por ID (sucesso e ID inexistente)
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
- Testes de contrato (schema validation) — identificado como melhoria futura via `jsonschema`

---

## 5. Cenários por Endpoint

Legenda: ✅ Implementado · ⬜ A implementar · 🟢 Sucesso · 🔴 Erro

### 5.1 `POST /login`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| L01 | 🟢 | Login com credenciais válidas | `test_login_success` | 200 + `authorization` no body | ✅ |
| L02 | 🔴 | Login com senha incorreta | `test_login_senha_errada` | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L03 | 🔴 | Login com e-mail inexistente | `test_login_email_inexistente` | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L04 | 🔴 | Login sem o campo `email` | `test_login_email_ausente_no_corpo` | 400 + `"email não pode ficar em branco"` | ✅ |
| L05 | 🔴 | Login sem o campo `password` | `test_login_senha_ausente_no_corpo` | 400 + `"password não pode ficar em branco"` | ✅ |
| L06 | 🔴 | Login com ambos os campos vazios | `test_login_campos_todos_ausentes` | 400 + ambas as mensagens de erro | ✅ |

### 5.2 `GET /usuarios`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U01 | 🟢 | Listar todos os usuários | `test_can_get_users` | 200 | ✅ |

### 5.3 `GET /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U02 | 🟢 | Buscar usuário por ID válido com validação de campos | `test_get_users_by_id` | 200 + campos corretos no body | ✅ |
| U03 | 🔴 | Buscar usuário com ID inexistente | `test_get_users_by_id_not_found` | 400 + `"Usuário não encontrado"` | ✅ |

### 5.4 `POST /usuarios`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U04 | 🟢 | Criar usuário com dados válidos | `test_create_user` | 201 + `_id` no body | ✅ |
| U05 | 🔴 | Criar usuário com e-mail já cadastrado | `test_create_user_email_em_uso` | 400 + `"Este email já está sendo usado"` | ✅ |
| U06 | 🔴 | Criar usuário com body vazio | `test_create_user_sem_body` | 400 + mensagens de campos obrigatórios | ✅ |
| U07 | 🔴 | Criar usuário com e-mail em formato inválido | `test_create_user_email_formato_inválido` | 400 + `"email deve ser um email válido"` | ✅ |

### 5.5 `PUT /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U08 | 🟢 | Atualizar usuário existente e verificar persistência | `test_update_user` | 200 + GET confirma alteração | ✅ |
| U09 | 🟢 | Atualizar usuário inexistente (upsert — cria novo) | `test_update_user_inexistente` | 201 + `_id` no body | ✅ |
| U10 | 🔴 | Atualizar para e-mail já usado por outro usuário | `test_update_user_email_em_uso` | 400 + `"Este email já está sendo usado"` | ✅ |
| U11 | 🔴 | Atualizar com campo obrigatório vazio | `test_update_user_campo_obrigatorio_ausente` | 400 + `"nome não pode ficar em branco"` | ✅ |

### 5.6 `DELETE /usuarios/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| U12 | 🟢 | Deletar usuário existente | `test_delete_user_success` | 200 + mensagem de exclusão | ✅ |
| U13 | 🟢 | Deletar usuário com ID inexistente | `test_delete_user_id_inexistente` | 200 + `"Nenhum registro excluído"` | ✅ |

> **Obs.:** A API retorna 200 (não 404) ao deletar um ID inexistente — comportamento documentado no teste `test_delete_user_id_inexistente`.

### 5.7 `GET /produtos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P01 | 🟢 | Listar todos os produtos | `test_can_get_product` | 200 | ✅ |
| P02 | 🟢 | Filtrar por query param `nome` | `test_get_product_parametro_nome` | 200 + lista filtrada corretamente | ✅ |

### 5.8 `GET /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P03 | 🟢 | Buscar produto por ID válido | `test_get_product_by_id` | 200 | ✅ |
| P04 | 🔴 | Buscar produto com ID inexistente | `test_get_product_by_id_inexistente` | 400 + `"Produto não encontrado"` | ✅ |

### 5.9 `POST /produtos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P05 | 🟢 | Criar produto como administrador | `test_can_create_product` | 201 + `_id` no body | ✅ |
| P06 | 🔴 | Criar produto como usuário não-admin | `test_criar_produto_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P07 | 🔴 | Criar produto sem header de autenticação | `test_criar_produto_sem_header_de_autenticacao` | 401 + mensagem de token ausente | ✅ |
| P08 | 🔴 | Criar produto com token inválido | `test_criar_produto_com_token_invalido` | 401 + mensagem de token inválido | ✅ |
| P09 | 🔴 | Criar produto com `nome` vazio | `test_criar_produto_sem_nome` | 400 + `"nome não pode ficar em branco"` | ✅ |
| P10 | 🔴 | Criar produto com `preco` vazio (string vazia) | `test_criar_produto_sem_preco` | 400 + `"preco deve ser um número"` | ✅ |
| P11 | 🔴 | Criar produto com `preco` negativo | `test_criar_produto_preco_negativo` | 400 + `"preco deve ser um número positivo"` | ✅ |
| P12 | 🔴 | Criar produto com `quantidade` negativa | `test_criar_produto_quantidade_negativa` | 400 + `"quantidade deve ser maior ou igual a 0"` | ✅ |

### 5.10 `PUT /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P13 | 🟢 | Atualizar produto existente como admin | `test_can_update_product` | 200 + `"Registro alterado com sucesso"` | ✅ |
| P14 | 🟢 | Atualizar produto inexistente como admin (upsert) | `test_can_update_product_inexistente` | 201 + `_id` no body | ✅ |
| P15 | 🔴 | Atualizar produto sem autenticação (token inválido) | `test_can_update_product_sem_token` | 401 + mensagem de token inválido | ✅ |
| P16 | 🔴 | Atualizar produto como usuário não-admin | `test_can_update_product_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P17 | 🔴 | Atualizar produto com nome já usado por outro produto | `test_can_update_product_mesmo_nome` | 400 + `"Já existe produto com esse nome"` | ✅ |

### 5.11 `DELETE /produtos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| P18 | 🟢 | Deletar produto existente como admin | `test_can_delete_product` | 200 + mensagem de exclusão | ✅ |
| P19 | 🟢 | Deletar produto com ID inexistente | `test_delete_produto_id_inexistente` | 200 + `"Nenhum registro excluído"` | ✅ |
| P20 | 🔴 | Deletar produto sem autenticação (token inválido) | `test_delete_produto_sem_autenticacao` | 401 + mensagem de token inválido | ✅ |
| P21 | 🔴 | Deletar produto como usuário não-admin | `test_delete_produto_sem_admin` | 403 + `"Rota exclusiva para administradores"` | ✅ |

### 5.12 `POST /carrinhos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C01 | 🟢 | Criar carrinho com produto válido | `test_create_cart` | 201 + `_id` no body | ✅ |
| C02 | � | Criar segundo carrinho para o mesmo usuário | — | 400 + `"Não é permitido ter mais de 1 carrinho"` | ⬜ |
| C03 | 🔴 | Criar carrinho com produto inexistente | — | 400 + `"Produto não encontrado"` | ⬜ |
| C04 | � | Criar carrinho com quantidade maior que o estoque | — | 400 + `"Produto não possui quantidade suficiente"` | ⬜ |
| C05 | 🔴 | Criar carrinho sem autenticação | — | 401 + mensagem de token ausente | ⬜ |
| C06 | 🔴 | Criar carrinho com produto duplicado na lista | — | 400 + `"Não é permitido possuir produto duplicado"` | ⬜ |

### 5.13 `GET /carrinhos`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C07 | 🟢 | Listar todos os carrinhos | — | 200 + lista no body | ⬜ |
| C08 | � | Filtrar carrinhos por `idUsuario` | — | 200 + lista filtrada | ⬜ |

### 5.14 `GET /carrinhos/:id`

| # | Tipo | Cenário | Teste | Status esperado | Impl. |
|---|---|---|---|---|---|
| C09 | � | Buscar carrinho por ID válido | — | 200 + `precoTotal` e `quantidadeTotal` corretos | ⬜ |
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
| C14 | 🟢 | Cancelar compra com carrinho ativo | — | 200 + estoque restaurado | ⬜ |
| C15 | 🟢 | Cancelar compra sem carrinho ativo | — | 200 + `"Não foi encontrado carrinho para esse usuário"` | ⬜ |
| C16 | 🔴 | Cancelar compra sem autenticação | — | 401 + mensagem de token ausente | ⬜ |

---

## 6. Critérios de Qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

1. **Isolado** — cria e remove seus próprios dados; não depende de estado pré-existente no ambiente.
2. **Determinístico** — passa e falha consistentemente nas mesmas condições; sem dependência de ordem de execução.
3. **Assertivo** — verifica status code HTTP *e* ao menos um campo relevante do corpo da resposta.
4. **Nomeado corretamente** — segue o padrão `test_<ação>_<recurso>_<condição>` em inglês.
5. **Sem vazamento de dados** — o teardown da fixture remove todos os recursos criados, mesmo que o teste falhe.
6. **Legível** — payload, chamada HTTP e asserções são visíveis no corpo do teste sem necessidade de abrir outros arquivos.
7. **Categorizado** — está no arquivo correto (`test_queries_` para leituras, `test_commands_` para escrita/deleção).

---

## 7. Melhorias Futuras

| Item | Descrição |
|---|---|
| Validação de schema | Substituir assertions de campos individuais por validação via `jsonschema` (anotado no `test_get_users_by_id`) |
