# from django.conf.urls import url
from django.urls import path, include
from .views import (
    NoteListApiView,
    NoteDetailApiView
)

urlpatterns = [
    path('api', NoteListApiView.as_view()),
    path('api/<int:note_id>/', NoteDetailApiView.as_view()),
]
