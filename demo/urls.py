from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save_image', views.save_image, name='save_image'),
    path('display_result', views.display_result, name='display_result'),
]