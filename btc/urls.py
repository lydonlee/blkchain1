from django.urls import path

from . import views

app_name = 'btc'
urlpatterns = [
    path('<str:coin_name>/', views.index, name='BTCindex'),
    path('', views.index, name='BTCindex')
]