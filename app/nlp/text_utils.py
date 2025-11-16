import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

STOPWORDS_PT = set(stopwords.words("portuguese"))

def preprocessar_texto(texto: str):
    tokens = word_tokenize(texto.lower(), language="portuguese")
    tokens_limpos = [t for t in tokens if t.isalpha() and t not in STOPWORDS_PT]
    return tokens_limpos

def classificar_email_simples(texto: str) -> str:
    tokens = preprocessar_texto(texto)

    palavras_produtivo = {"status", "suporte", "problema", "erro", "atraso", "andamento", "reclamação", "dúvida", "prazo"}
    palavras_improdutivo = {"obrigado", "agradeço", "parabéns", "feliz", "natal", "bom", "dia", "tarde", "noite"}

    tem_produtivo = any(p in tokens for p in palavras_produtivo)
    tem_improdutivo = any(p in tokens for p in palavras_improdutivo)

    if tem_produtivo and not tem_improdutivo:
        return "Produtivo"
    elif tem_improdutivo and not tem_produtivo:
        return "Improdutivo"
    elif tem_produtivo and tem_improdutivo:
        return "Produtivo"
    else:
        return "Produtivo"
