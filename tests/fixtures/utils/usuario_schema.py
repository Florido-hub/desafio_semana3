USUARIO_SCHEMA = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "administrador": {"type": "string"},
                    "_id": {"type": "string"}
                },
                "required": [
                    "nome",
                    "email",
                    "password",
                    "administrador",
                    "_id"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": ["quantidade", "usuarios"]
}

USUARIO_SCHEMA_ID = {
  "type": "object",
  "properties": {
    "nome": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "password": {
      "type": "string"
    },
    "administrador": {
      "type": "string"
    },
    "_id": {
      "type": "string"
    }
  },
  "required": [
    "nome",
    "email",
    "password",
    "administrador",
    "_id"
  ]
}