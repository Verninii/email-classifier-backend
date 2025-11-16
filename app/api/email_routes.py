from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.email import EmailRequest, EmailResponse
from app.services.email_service import (
    classificar_email_ia,
    gerar_resposta_ia,
    extrair_texto_de_arquivo,
)

router = APIRouter()

@router.post("/analyze", response_model=EmailResponse)
def analyze_email(request: EmailRequest):
    texto = request.texto

    categoria = classificar_email_ia(texto)
    resposta = gerar_resposta_ia(texto, categoria)

    return EmailResponse(
        categoria=categoria,
        resposta_sugerida=resposta,
    )

@router.post("/analyze_file", response_model=EmailResponse)
def analyze_email_file(file: UploadFile = File(...)):
    texto = extrair_texto_de_arquivo(file)

    if not texto.strip():
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto do arquivo.")

    categoria = classificar_email_ia(texto)
    resposta = gerar_resposta_ia(texto, categoria)

    return EmailResponse(
        categoria=categoria,
        resposta_sugerida=resposta,
    )
