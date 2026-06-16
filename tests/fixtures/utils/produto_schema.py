PRODUTO_SCHEMA = {
    "type": "object",
    "properties": {
        "quantidade": {
            "type": "integer"
        },
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string"
                    },
                    "preco": {
                        "type": "integer"
                    },
                    "descricao": {
                        "type": "string"
                    },
                    "quantidade": {
                        "type": "integer"
                    },
                    "_id": {
                        "type": "string"
                    }
                },
                "required": [
                    "nome",
                    "preco",
                    "descricao",
                    "quantidade",
                    "_id"
                ]
            }
        }
    },
    "required": [
        "quantidade",
        "produtos"
    ]
}


PRODUTO_SCHEMA_ID = {
  "type": "object",
  "properties": {
    "nome": {
      "type": "string"
    },
    "preco": {
      "type": "integer"
    },
    "descricao": {
      "type": "string"
    },
    "quantidade": {
      "type": "integer"
    },
    "_id": {
      "type": "string"
    }
  },
  "required": [
    "nome",
    "preco",
    "descricao",
    "quantidade",
    "_id"
  ]
}