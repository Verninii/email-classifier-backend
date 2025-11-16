# 📧 Email Classifier – Backend (FastAPI + NLP + IA)

Backend em **FastAPI** responsável por:

- Ler e pré-processar o texto de e-mails (texto puro ou arquivos `.txt` / `.pdf`)
- Classificar cada e-mail como **Produtivo** ou **Improdutivo**
- Gerar uma **resposta automática** usando IA (OpenAI) ou respostas padrão (fallback)

---

O backend em FastAPI está neste repositório:
https://github.com/Verninii/email-classifier-backend

API publicada:
https://email-classifier-backend-9w9c.onrender.com

---

## 🧠 Tecnologias utilizadas

- **Python 3.10+**
- **FastAPI** (API web)
- **Uvicorn** (servidor ASGI)
- **NLTK** (pré-processamento de linguagem natural)
- **OpenAI API** (geração de resposta automática – opcional)
- Biblioteca para leitura de PDFs (`pdfplumber` ou similar)
- **Pydantic** (validação de dados)
- **CORS Middleware** (integração segura com o frontend no Vercel)

---

🛠️ Como rodar localmente

1️⃣ Clonar o repositório
git clone https://github.com/Verninii/email-classifier-backend.git
cd email-classifier-backend

2️⃣ Criar e ativar o ambiente virtual

Windows:

python -m venv venv
venv\Scripts\activate

Linux / MacOS:

python3 -m venv venv
source venv/bin/activate

3️⃣ Instalar as dependências
pip install -r requirements.txt

4️⃣ Configurar a chave da OpenAI (opcional, mas recomendado)

Crie um arquivo .env na raiz do projeto:

OPENAI_API_KEY=sua-chave-aqui

Se a variável não estiver configurada ou der erro na chamada da API, o sistema utiliza classificação simples por regras e respostas padrão (fallback), mantendo a API funcional.

5️⃣ Rodar o servidor
uvicorn app.main:app --reload

A API ficará disponível em:

Swagger (documentação): http://127.0.0.1:8000/docs

Root: http://127.0.0.1:8000/

🚀 Deploy

API: Render → https://email-classifier-backend-9w9c.onrender.com

Frontend: Vercel → https://email-classifier-frontend-flax.vercel.app

O frontend consome este backend através de chamadas fetch em:

POST /analyze

POST /analyze_file

🧩 Observações

Caso a IA da OpenAI esteja sem crédito/quota, a API continua funcionando com:

Classificação baseada em palavras-chave

Respostas padrão de acordo com a categoria
