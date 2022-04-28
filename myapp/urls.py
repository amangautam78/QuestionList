from django.urls import path
from .views import QuestionList, CreateQuestion, UpdateQuestion
urlpatterns = [
    path('question-list/',  QuestionList.as_view()),
    path('add/', CreateQuestion.as_view()),
    path('question/<int:id>/', UpdateQuestion.as_view())
]