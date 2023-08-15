from django.urls import path
from sumarizar.views import index, sumarizer, sumarizar_texto
from . import views

urlpatterns = [
    path('', index),
    path('sumarizar/sumarizer-page.html', sumarizer),
    path('sumarizar_texto', views.sumarizar_texto, name='sumarizar_texto'),
    path('obter_informacoes_texto', views.obter_informacoes_texto, name='obter_informacoes_texto')
]
    