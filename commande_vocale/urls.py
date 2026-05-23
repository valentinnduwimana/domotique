from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/led/', views.control_led, name='control_led'),
]