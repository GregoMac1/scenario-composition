from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('<int:project_id>/composition/', views.project_episode_composition, name='project_composition'),
    path('<int:project_id>/scenarios/create/', views.create_scenario, name='create_scenario'),
    path('<int:project_id>/scenarios/<int:scenario_id>/edit/', views.edit_scenario, name='edit_scenario'),
    path('<int:project_id>/scenarios/<int:scenario_id>/delete/', views.delete_scenario, name='delete_scenario'),
    path('<int:project_id>/scenarios/<int:scenario_id>/tree/', views.episode_tree, name='episode_tree'),
    path('<int:project_id>/dictionary/', views.dictionary_list, name='dictionary_list'),
    path('<int:project_id>/dictionary/create/', views.create_dictionary_term, name='create_dictionary_term'),
    path('<int:project_id>/dictionary/<int:term_id>/edit/', views.edit_dictionary_term, name='edit_dictionary_term'),
    path('<int:project_id>/dictionary/<int:term_id>/delete/', views.delete_dictionary_term, name='delete_dictionary_term'),
]
