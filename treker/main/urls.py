from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('syntax', views.syntax),
    path('runtime', views.runtime),
    path('prog/<str:prg_name>', views.prog),
    path('upload', views.upload),
    path('download', views.download_file),
    path('download/<str:p_name>', views.file_send),
    path('syntax/<str:p_name>/<str:time>', views.syntax),
    path('runtime/<str:p_name>/<str:time>', views.runtime),
    path('how_use',views.how_use),
    path('delite/<str:p_name>',views.delite)
]
