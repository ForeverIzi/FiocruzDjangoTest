from django.shortcuts import render
from sumarizar.sumarizar import sumarize, detect_redundancy, quantidade_de_sent
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

def sumarizer(request):
    return render(request, 'sumarizer-page.html')


def sumarizar_texto(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        num_sentencas = int(request.POST.get('num_sentencas'))
        sumarizador = sumarize(texto, num_sentencas)
        resumo, sentencas, melhores_sentencas = sumarizador

        palavras_redundantes = detect_redundancy(texto)  # Aqui chamamos a função para obter as palavras redundantes

        response_data = {'resumo': resumo }

        return JsonResponse(response_data)
    else:
        return render(request, 'form.html')

def obter_informacoes_texto(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        num_sentencas = int(request.POST.get('num_sentencas'))

        melhores_sentencas = []
        palavras_redundantes = []

        if texto:
            melhores_sentencas = sumarize(texto, num_sentencas)[2]  # Terceiro valor retornado pela função sumarize
            palavras_redundantes = detect_redundancy(texto)  # Função para obter palavras redundantes

        num_sentencas_calculado = quantidade_de_sent(texto, num_sentencas)  # Calcula a quantidade de sentenças

        response_data = {
            'melhores_sentencas': melhores_sentencas,
            'num_sentencas': num_sentencas_calculado,
            'palavras_redundantes': palavras_redundantes
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Método inválido'})

    
     
"""
def sumarizar_texto(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        num_sentencas = request.POST.get('num_sentencas')
        sumarizador = sumarize(texto, num_sentencas)
        resumo, sentencas, melhores_sentencas = sumarizador.sumarize(texto, num_sentencas)

        # Retornar a resposta em JSON
        response_data = {'resumo': resumo}
        return JsonResponse(response_data)
    else:
        return render(request, 'form.html')

    """
    
