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
- `GET /usuarios` — listagem de usuários
- `GET /usuarios/:id` — busca por ID (sucesso e ID inexistente)
- `POST /usuarios` — cadastro de usuário (sucesso e e-mail duplicado)
- `DELETE /usuarios/:id` — remoção de usuário (via teardown de fixture)
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
- `PUT /usuarios/:id` — atualização de usuário não implementada
- Testes de carga ou performance
- Testes de contrato (schema validation) — identificado como melhoria futura (`#Melhorar aqui usando o rolê do schema`)
- Testes de segurança (ex.: injeção, tokens expirados)

---

## 4. Cenários por Endpoint

Legenda: ✅ Implementado · ⬜ A implementar

### 4.1 `POST /login`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| L01 | Login com credenciais válidas | 200 + token no body | ✅ |
| L02 | Login com senha incorreta | 401 + mensagem de erro | ✅ |
| L03 | Login com e-mail inexistente | 401 | ⬜ |
| L04 | Login com body vazio / campos ausentes | 400 | ⬜ |

### 4.2 `GET /usuarios`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| U01 | Listar todos os usuários | 200 | ✅ |
| U02 | Filtrar por query param `administrador=true` | 200 + lista filtrada | ⬜ |

### 4.3 `GET /usuarios/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| U04 | Buscar usuário por ID válido | 200 + dados corretos | ✅ |
| U05 | Buscar usuário com ID inexistente | 400 | ✅ |

### 4.4 `POST /usuarios`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| U06 | Criar usuário administrador com dados válidos | 201 + `_id` no body | ✅ |
| U07 | Criar usuário com e-mail já cadastrado | 400 + mensagem de erro | ✅ |
| U08 | Criar usuário com campos obrigatórios ausentes | 400 | ⬜ |
| U09 | Criar usuário não-administrador | 201 | ⬜ |

### 4.5 `PUT /usuarios/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| U10 | Atualizar dados de um usuário existente | 200 | ⬜ |
| U11 | Atualizar usuário inexistente (deve criar) | 201 | ⬜ |

### 4.6 `DELETE /usuarios/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| U12 | Deletar usuário existente | 200 | ⬜ (coberto via teardown) |
| U13 | Deletar usuário com carrinho ativo | 400 | ⬜ |

### 4.7 `GET /produtos`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| P01 | Listar todos os produtos | 200 | ✅ |
| P02 | Filtrar por query param `nome` | 200 + lista filtrada | ⬜ |

### 4.8 `GET /produtos/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| P03 | Buscar produto por ID válido | 200 | ✅ |
| P04 | Buscar produto com ID inexistente | 400 | ⬜ |

### 4.9 `POST /produtos`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| P05 | Criar produto como administrador | 201 + `_id` no body | ✅ |
| P06 | Criar produto sem token de autenticação | 401 | ⬜ |
| P07 | Criar produto como usuário não-admin | 403 + mensagem de erro | ✅ |
| P08 | Criar produto com nome duplicado | 400 | ⬜ |

### 4.10 `PUT /produtos/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| P09 | Atualizar produto existente como admin | 200 | ✅ |
| P10 | Atualizar produto sem autenticação | 401 | ⬜ |
| P11 | Atualizar produto como não-admin | 403 | ⬜ |

### 4.11 `DELETE /produtos/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| P12 | Deletar produto existente como admin | 200 | ✅ |
| P13 | Deletar produto com estoque em carrinho | 400 | ⬜ |
| P14 | Deletar produto sem autenticação | 401 | ⬜ |

### 4.12 `GET /carrinhos`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| C01 | Listar todos os carrinhos | 200 | ⬜ |
| C02 | Filtrar carrinhos por `idUsuario` | 200 + lista filtrada | ⬜ |

### 4.13 `GET /carrinhos/:id`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| C03 | Buscar carrinho por ID válido | 200 + itens corretos | ⬜ |
| C04 | Buscar carrinho com ID inexistente | 400 | ⬜ |

### 4.14 `POST /carrinhos`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| C05 | Criar carrinho com produto válido | 201 + `_id` no body | ⬜ |
| C06 | Criar segundo carrinho para o mesmo usuário | 400 | ⬜ |
| C07 | Criar carrinho com produto inexistente | 400 | ⬜ |
| C08 | Criar carrinho com quantidade maior que o estoque | 400 | ⬜ |
| C09 | Criar carrinho sem autenticação | 401 | ⬜ |

### 4.15 `DELETE /carrinhos/concluir-compra`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| C10 | Concluir compra com carrinho ativo | 200 + estoque decrementado | ⬜ |
| C11 | Concluir compra sem carrinho ativo | 200 (sem efeito) | ⬜ |

### 4.16 `DELETE /carrinhos/cancelar-compra`

| # | Cenário | Status esperado | Status |
|---|---|---|---|
| C12 | Cancelar compra com carrinho ativo | 200 + estoque restaurado | ⬜ |
| C13 | Cancelar compra sem carrinho ativo | 200 (sem efeito) | ⬜ |

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
