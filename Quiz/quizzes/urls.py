from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-questions/', views.add_questions, name='add_questions'),
    path('quiz/<int:quiz_id>/finish/', views.finish_quiz_creation, name='finish_quiz_creation'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    
    # Edycja quizu
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    
    # Usuwanie quizu
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),

    # Edycja pytania
    path('quiz/<int:quiz_id>/question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    
    # Usuwanie pytania
    path('quiz/<int:quiz_id>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),



]
