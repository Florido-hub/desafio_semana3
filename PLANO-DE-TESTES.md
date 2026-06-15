# Plano de Testes — ServeRest API

## 1. Objetivo

Validar o comportamento da API ServeRest (`https://compassuol.serverest.dev/`) nos quatro domínios principais — Login, Usuários, Produtos e Carrinhos — garantindo que os contratos de resposta, os códigos HTTP, as regras de negócio e os controles de acesso estejam funcionando conforme o esperado.

---

## 2. Estratégia

| Aspecto | Decisão |
|---|---|
| Tipo de teste | Testes funcionais de API (caixa-preta) |
| Camada | Integração — chamadas HTTP diretas ao ambiente remoto |
| Ferramentas | Python 3 · pytest · requests |
| Abordagem | Arrange → Act → Assert: cada teste cria seus dados via fixture, executa a ação e verifica status code + corpo da resposta |
| Isolamento | Fixtures com `yield` garantem criação e limpeza (teardown) automáticas por teste |
| Dados dinâmicos | Nomes e e-mails únicos gerados com `int(time.time())` para evitar colisões entre execuções |
| Ambiente | Somente ambiente remoto compartilhado (sem mock, sem ambiente local) |

---

## 3. Escopo

### 3.1 Coberto

- `POST /login` — autenticação com credenciais válidas e inválidas
- `GET /usuarios` — listagem e filtro por `administrador`
- `GET /usuarios/:id` — busca por ID (sucesso e ID inexistente)
- `POST /usuarios` — cadastro de usuário (sucesso e e-mail duplicado)
- `PUT /usuarios/:id` — atualização de usuário (sucesso)
- `DELETE /usuarios/:id` — remoção de usuário (via teardown de fixture e teste explícito)
- `GET /produtos` — listagem de produtos
- `GET /produtos/:id` — busca de produto por ID
- `POST /produtos` — cadastro de produto (admin e não-admin)
- `PUT /produtos/:id` — atualização de produto
- `DELETE /produtos/:id` — remoção de produto

### 3.2 Fora do escopo

- `GET /carrinhos` — não implementado ainda
- `GET /carrinhos/:id` — não implementado ainda
- `POST /carrinhos` — não implementado ainda
- `DELETE /carrinhos/concluir-compra` — não implementado ainda
- `DELETE /carrinhos/cancelar-compra` — não implementado ainda
- Testes de carga ou performance
- Testes de contrato (schema validation) — identificado como melhoria futura
- Testes de segurança (ex.: injeção, tokens expirados)

---

## 4. Cenários por Endpoint

Legenda: ✅ Implementado · ⬜ A implementar · 🟢 Sucesso · 🔴 Erro

### 4.1 `POST /login`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| L01 | 🟢 | Login com credenciais válidas | 200 + `authorization` no body | ✅ |
| L02 | 🔴 | Login com senha incorreta | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L03 | 🔴 | Login com e-mail inexistente | 401 + `"Email e/ou senha inválidos"` | ✅ |
| L04 | 🔴 | Login sem o campo `email` no body | 400 + `"email não pode ficar em branco"`| ✅ |
| L05 | 🔴 | Login sem o campo `password` no body | 400 + `"password não pode ficar em branco"`| ✅ |
| L06 | 🔴 | Login com body vazio `{}` | 400 | ✅ |

### 4.2 `GET /usuarios`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| U01 | 🟢 | Listar todos os usuários | 200 + lista no body | ✅ |
| U02 | 🟢 | Filtrar por `administrador=true` | 200 + todos os itens com `administrador=true` | ✅ |
| U03 | 🟢 | Filtrar por `administrador=false` | 200 + todos os itens com `administrador=false` | ✅ |

### 4.3 `GET /usuarios/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| U04 | 🟢 | Buscar usuário por ID válido | 200 + dados corretos no body | ✅ |
| U05 | 🔴 | Buscar usuário com ID inexistente | 400 + `"Usuário não encontrado"` | ✅ |

### 4.4 `POST /usuarios`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| U06 | 🟢 | Criar usuário administrador com dados válidos | 201 + `_id` no body | ✅ |
| U07 | 🔴 | Criar usuário com e-mail já cadastrado | 400 + `"Este email já está sendo usado"` | ✅ |
| U08 | 🔴 | Criar usuário com body vazio `{}` | 400 + mensagem de campo obrigatório | ✅ |
| U11 | 🔴 | Criar usuário com e-mail em formato inválido | 400 + mensagem de validação | ✅ |

### 4.5 `PUT /usuarios/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| U13 | 🟢 | Atualizar dados de um usuário existente | 200 + `"Registro alterado com sucesso"` | ✅ |
| U14 | 🟢 | Atualizar usuário inexistente (upsert — deve criar) | 201 + `_id` no body | ✅ |
| U15 | 🔴 | Atualizar para um e-mail já usado por outro usuário | 400 + `"Este email já está sendo usado"` | ✅ |
| U16 | 🔴 | Atualizar usuário com campo obrigatório ausente | 400 | ✅ |

### 4.6 `DELETE /usuarios/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| U17 | 🟢 | Deletar usuário existente sem carrinho | 200 + `"Registro excluído com sucesso"` | ✅ |
| U18 | 🟢 | Deletar usuário com ID inexistente | 200 + `"Nenhum registro excluído"` | ✅ |

### 4.7 `GET /produtos`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| P01 | 🟢 | Listar todos os produtos | 200 + lista no body | ✅ |
| P02 | 🟢 | Filtrar por query param `nome` | 200 + lista filtrada | ✅ |

### 4.8 `GET /produtos/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| P03 | 🟢 | Buscar produto por ID válido | 200 + dados corretos | ✅ |
| P04 | 🔴 | Buscar produto com ID inexistente | 400 + `"Produto não encontrado"` | ✅ |

### 4.9 `POST /produtos`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| P05 | 🟢 | Criar produto como administrador com dados válidos | 201 + `_id` no body | ✅ |
| P06 | 🔴 | Criar produto como usuário não-admin | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P07 | 🔴 | Criar produto sem header de autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ✅ |
| P08 | 🔴 | Criar produto com token inválido / expirado | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ✅ |
| P09 | 🔴 | Criar produto sem o campo `nome` | 400 + mensagem de campo obrigatório | ✅ |
| P10 | 🔴 | Criar produto sem o campo `preco` | 400 + mensagem de campo obrigatório | ✅ |
| P11 | 🔴 | Criar produto com `preco` negativo ou zero | 400 + mensagem de validação | ✅ |
| P12 | 🔴 | Criar produto com `quantidade` negativa | 400 + mensagem de validação | ✅ |

### 4.10 `PUT /produtos/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| P14 | 🟢 | Atualizar produto existente como admin | 200 + `"Registro alterado com sucesso"` | ✅ |
| P15 | 🟢 | Atualizar produto inexistente como admin (upsert) | 201 + `_id` no body | ✅ |
| P16 | 🔴 | Atualizar produto sem autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ✅ |
| P17 | 🔴 | Atualizar produto como usuário não-admin | 403 + `"Rota exclusiva para administradores"` | ✅ |
| P18 | 🔴 | Atualizar produto com nome já usado por outro produto | 400 + `"Já existe produto com esse nome"` | ✅ |

### 4.11 `DELETE /produtos/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| P19 | 🟢 | Deletar produto existente como admin | 200 + `"Registro excluído com sucesso"` | ✅ |
| P20 | 🔴 | Deletar produto que está em carrinho ativo | 400 + `"Não é permitido excluir produto que faz parte do carrinho"` | ⬜ |
| P21 | 🔴 | Deletar produto sem autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ⬜ |
| P22 | 🔴 | Deletar produto como usuário não-admin | 403 + `"Rota exclusiva para administradores"` | ⬜ |
| P23 | 🟢 | Deletar produto com ID inexistente | 200 + `"Nenhum registro excluído"` | ⬜ |

### 4.12 `GET /carrinhos`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| C01 | 🟢 | Listar todos os carrinhos | 200 + lista no body | ⬜ |
| C02 | 🟢 | Filtrar carrinhos por `idUsuario` | 200 + lista filtrada | ⬜ |

### 4.13 `GET /carrinhos/:id`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| C03 | 🟢 | Buscar carrinho por ID válido | 200 + itens, `precoTotal` e `quantidadeTotal` corretos | ⬜ |
| C04 | 🔴 | Buscar carrinho com ID inexistente | 400 + `"Carrinho não encontrado"` | ⬜ |

### 4.14 `POST /carrinhos`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| C05 | 🟢 | Criar carrinho com produto válido | 201 + `_id` no body | ⬜ |
| C06 | 🔴 | Criar segundo carrinho para o mesmo usuário | 400 + `"Não é permitido ter mais de 1 carrinho"` | ⬜ |
| C07 | 🔴 | Criar carrinho com produto inexistente | 400 + `"Produto não encontrado"` | ⬜ |
| C08 | 🔴 | Criar carrinho com quantidade maior que o estoque | 400 + `"Produto não possui quantidade suficiente"` | ⬜ |
| C09 | 🔴 | Criar carrinho sem autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ⬜ |
| C10 | 🔴 | Criar carrinho com produto duplicado na lista | 400 + `"Não é permitido possuir produto duplicado"` | ⬜ |

### 4.15 `DELETE /carrinhos/concluir-compra`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| C11 | 🟢 | Concluir compra com carrinho ativo | 200 + `"Registro excluído com sucesso"` + estoque decrementado | ⬜ |
| C12 | 🟢 | Concluir compra sem carrinho ativo | 200 + `"Não foi encontrado carrinho para esse usuário"` | ⬜ |
| C13 | 🔴 | Concluir compra sem autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ⬜ |

### 4.16 `DELETE /carrinhos/cancelar-compra`

| # | Tipo | Cenário | Status esperado | Impl. |
|---|---|---|---|---|
| C14 | 🟢 | Cancelar compra com carrinho ativo | 200 + `"Registro excluído com sucesso"` + estoque restaurado | ⬜ |
| C15 | 🟢 | Cancelar compra sem carrinho ativo | 200 + `"Não foi encontrado carrinho para esse usuário"` | ⬜ |
| C16 | 🔴 | Cancelar compra sem autenticação | 401 + `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"` | ⬜ |

---

## 5. Critérios de Qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

1. **Isolado** — cria e remove seus próprios dados; não depende de estado pré-existente no ambiente.
2. **Determinístico** — passa e falha consistentemente nas mesmas condições; sem dependência de ordem de execução.
3. **Assertivo** — verifica status code HTTP *e* ao menos um campo relevante do corpo da resposta.
4. **Nomeado corretamente** — segue o padrão `test_<ação>_<recurso>_<condição>` em inglês.
5. **Sem vazamento de dados** — o teardown da fixture remove todos os recursos criados, mesmo que o teste falhe.
6. **Legível** — payload, chamada HTTP e asserções são visíveis no corpo do teste sem necessidade de abrir outros arquivos.
7. **Categorizado** — está no arquivo correto (`test_queries_` para leituras, `test_commands_` para escrita/deleção).
