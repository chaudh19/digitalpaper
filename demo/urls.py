from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mathpix_lookup', views.mathpix_lookup, name='mathpix_lookup'),
    path('wolfram_expanded_form', views.wolfram_expanded_form, name='wolfram_expanded_form'),
    path('wolfram_evaluate', views.wolfram_evaluate, name='wolfram_evaluate'),
    path('wolfram_terms', views.wolfram_terms, name='wolfram_terms'),
    path('wolfram', views.wolfram, name='wolfram'),
    path('perms', views.perms, name='perms'),
    path('bootstrap/<int:num>', views.bootstrap, name='bootstrap'),
    path('bootstrap_query', views.bootstrap_query, name='bootstrap_query'),


    path('test_1', views.test_1, name='test_1'),
    
]