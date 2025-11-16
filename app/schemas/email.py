from pydantic import BaseModel

class EmailRequest(BaseModel):
    texto: str

class EmailResponse(BaseModel):
    categoria: str
    resposta_sugerida: str