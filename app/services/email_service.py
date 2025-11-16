import os
import io
from fastapi import UploadFile, HTTPException
from openai import OpenAI
import pdfplumber

from app.nlp.text_utils import classificar_email_simples

# Cliente OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def classificar_email_ia(texto: str) -> str:
    """
    Usa OpenAI para classificar entre Produtivo / Improdutivo.
    Cai na regra simples se não houver client ou se der erro.
    """
    if not client:
        return classificar_email_simples(texto)

    system_prompt = """
Você é um sistema de classificação de emails de uma empresa do setor financeiro.
Classifique o email em UMA categoria:

- Produtivo
- Improdutivo

Responda APENAS com "Produtivo" ou "Improdutivo".
"""

    user_prompt = f'Email:\n"""{texto}"""'

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )
        resp = completion.choices[0].message.content.strip().lower()

        if resp.startswith("produt"):
            return "Produtivo"
        if resp.startswith("improd"):
            return "Improdutivo"

        return classificar_email_simples(texto)

    except Exception as e:
        print("Erro na classificação IA:", e)
        return classificar_email_simples(texto)


def gerar_resposta_ia(texto: str, categoria: str) -> str:
    """
    Usa IA para sugerir resposta automática.
    Se não tiver client ou der erro, usa fallback.
    """
    def fallback(cat: str) -> str:
        if cat == "Improdutivo":
            return "Olá! Agradecemos sua mensagem e desejamos o mesmo em dobro. 😊"
        return "Olá! Recebemos sua solicitação e em breve retornaremos com uma atualização sobre o seu pedido."

    if not client:
        return fallback(categoria)

    system_prompt = """
Você é um assistente de atendimento ao cliente de uma empresa do setor financeiro.
Gere respostas educadas e profissionais em português do Brasil.
"""

    user_prompt = f"""
Categoria do email: {categoria}
Conteúdo do email:
\"\"\"{texto}\"\"\"

Gere apenas a resposta automática que será enviada ao cliente.
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
Você é um assistente de atendimento ao cliente de uma empresa do setor financeiro.
Sua tarefa:

- Se IMPRODUTIVO: responda curto, simpático, agradecendo.
- Se PRODUTIVO: agradeça o contato, confirme recebimento, diga que será analisado em breve.
Não invente dados específicos.
"""},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("Erro na resposta IA:", e)
        return fallback(categoria)


def extrair_texto_de_arquivo(file: UploadFile) -> str:
    """
    Lê um .txt ou .pdf e devolve o texto.
    """
    if file.content_type == "text/plain":
        conteudo_bytes = file.file.read()
        return conteudo_bytes.decode("utf-8", errors="ignore")

    if file.content_type == "application/pdf":
        conteudo_bytes = file.file.read()
        with pdfplumber.open(io.BytesIO(conteudo_bytes)) as pdf:
            paginas = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(paginas)

    raise HTTPException(
        status_code=400,
        detail="Tipo de arquivo não suportado. Envie um .txt ou .pdf.",
    )
