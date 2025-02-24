from django.urls import path
from .views import NoteListCreateView, NoteDelete, AnswerView
urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('questions/', AnswerView.as_view(), name='answer-question'),
]