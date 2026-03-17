from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('create/', views.exam_create, name='exam_create'),
    path('analytics/', views.teacher_analytics, name='teacher_analytics'),
    path('results/', views.result_list, name='result_list'),
    path('results/<int:pk>/', views.result_detail, name='result_detail'),
    path('<int:pk>/', views.exam_detail, name='exam_detail'),
    path('<int:pk>/edit/', views.exam_update, name='exam_update'),
    path('<int:pk>/delete/', views.exam_delete, name='exam_delete'),
    path('<int:exam_id>/instructions/', views.exam_instructions, name='exam_instructions'),
    path('<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('<int:exam_id>/question/add/', views.question_create, name='question_create'),
    path('question/<int:pk>/edit/', views.question_update, name='question_update'),
    path('question/<int:pk>/delete/', views.question_delete, name='question_delete'),
]