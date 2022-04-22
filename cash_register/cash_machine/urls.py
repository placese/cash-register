from django.urls import path

from . import views

urlpatterns = [
    path('cash_machine/', views.create_receipt, name='create_receipt'),
    path('media/<str:receipt>', views.get_receipt, name='get_receipt')
]