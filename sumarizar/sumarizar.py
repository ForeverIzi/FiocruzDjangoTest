from deepmultilingualpunctuation import PunctuationModel
import heapq
import re
import string
import nltk
import spacy


import gensim
import transformers

import numpy as np

nltk.download('punkt')
nltk.download("stopwords")
nlp = spacy.load("pt_core_news_sm")
model = PunctuationModel(model="kredor/punctuate-all")

def format_text(txt):
    txt = re.sub(r'\s', ' ', txt)
    txt = txt.replace("\\n\\n", " ")
    txt = txt.lower()
    tokens = []
    vicios = ['né', 'então', 'gente']
    stopwords = nltk.corpus.stopwords.words("portuguese") + vicios

    for i in nltk.word_tokenize(txt):
        if i not in stopwords and i not in string.punctuation:
            tokens.append(i)

    texto_formatado = " ".join(elemento for elemento in tokens if not elemento.isdigit())
    return texto_formatado

# Função para determinar se um ponto é um ponto final
def is_end_of_sentence(token):
    if token.i < len(token.doc) - 1:
        next_token = token.doc[token.i + 1]
        if next_token.is_title or next_token.is_upper:
            return True
    return False

def detect_redundancy(text):
    doc = nlp(text)
    redundant_words = []

    ignored_words = set(['e', 'ou', 'de', 'do', 'da', 'em', 'para', 'com', 'por', 'sem', 'sob', 'sobre', 'a', 'o', 'um', 'uma', 'seu', 'sua', 'seus', 'suas', 'nos', 'nas', 'no', 'na','()','(',')','entre','ao',','])

    for para in doc.sents:
        words_seen = set()
        for token in para:
            if token.text.lower() in words_seen:
                if token.text.lower() not in ignored_words:
                    if not is_end_of_sentence(token):
                        redundant_words.append(token.text)
            else:
                words_seen.add(token.text.lower())

    return redundant_words

# Sumarizar texto
def sumarize(text, quant_sentencas):
    # Pré-processe o texto
    text = nltk.sent_tokenize(text)
    text = [nltk.word_tokenize(sentença) for sentença in text]

    # Crie um modelo de linguagem
    model = transformers.AutoModelForSeq2SeqLM.from_pretrained("t5-base")

    # Gere um resumo
    resumo = model.generate(text)

    # Classifique as sentenças do resumo
    sentencas_resumo = nltk.sent_tokenize(resumo)
    nota_sentenca = {}
    for sentenca in sentencas_resumo:
        for palavra in nltk.word_tokenize(sentenca):
            if palavra in freq_palavras.keys():
                if sentenca not in nota_sentenca:
                    nota_sentenca[sentenca] = freq_palavras[palavra]
                else:
                    nota_sentenca[sentenca] += freq_palavras[palavra]

        melhores_sentencas = heapq.nlargest(quant_sentencas, nota_sentenca, key=nota_sentenca.get)

    # Ordene as sentenças do resumo
    sentencas_resumo_ordenadas = order_sentences(sentencas_resumo)

    # Combine o resumo do modelo com as sentenças selecionadas
    resumo = ""
    for sentenca in sentencas_resumo_ordenadas:
        resumo += sentenca

    # Adicione as sentenças selecionadas pelo seu código
    resumo += " ".join(sentenca for sentenca in sentencas_txt if sentenca in melhores_sentencas)
            
    return resumo, sentencas_txt, melhores_sentencas

# Função para calcular a quantidade de sentenças a serem mantidas no resumo
def quantidade_de_sent(text, num):
    num_sent = len(nltk.sent_tokenize(text))
    quant = (num_sent * num) / 100
    return round(quant)

"""
texto = input("Insira o texto para ser resumido: ")
num_sentencas = int(input("Insira a porcentagem de sentenças que deseja no resumo (em número inteiro): "))

resumo, sentencas, melhores_sentencas = sumarize(texto, quantidade_de_sent(texto, num_sentencas))

print(f"\nTexto resumido com ({num_sentencas}% das sentenças originais):\n{resumo}\n")

print("Todas as sentenças:")
for sentenca in sentencas:
    print(f"- {sentenca}")

print("\nMelhores sentenças:")
for sentenca in melhores_sentencas:
    print(f"- {sentenca}")

# Detectar palavras redundantes
redundant_words = detect_redundancy(texto)

if len(redundant_words) > 0:
    print("\nPalavras redundantes encontradas:")
    for word in redundant_words:
        print("- " + word)
else:
    print("\nNenhuma palavra redundante encontrada.")
"""