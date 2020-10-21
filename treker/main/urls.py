from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('syntax', views.syntax),
    path('runtime', views.runtime ),
    path('prog/<str:prg_name>', views.prog),
]
