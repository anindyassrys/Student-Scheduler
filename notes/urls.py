from django.urls import path
from notes.views import *

urlpatterns = [
    path('', get_notes, name='notes'),
    path('notes/create', create_notes, name='create_notes'),
    path('notes/<id>', get_detail_notes, name='detail_notes'),
    #path('notes/<id>/update', update_notes, name='update_notes'),
    path('notes/<id>/delete', delete_notes, name='delete_notes'),
]