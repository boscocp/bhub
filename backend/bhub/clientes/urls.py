from django.urls import path

from . import views

urlpatterns = [
    path('clientes/', views.ClienteCreateView.as_view()),
    path('clientes/<uuid:pk>', views.ClienteCreateView.as_view()),
    path('clientes/<uuid:pk>/', views.ClienteCreateView.as_view()),
    path('clientes/<uuid:pk>/dadosbancarios/', views.DadosBancariosCreateView.as_view()),
    path('clientes/<uuid:pk>/dadosbancarios/<db_id>/', views.DadosBancariosCreateView.as_view(), name='dadosbancarios'),
]