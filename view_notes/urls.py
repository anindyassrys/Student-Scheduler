from django.urls import path
from view_notes.views import *

urlpatterns = [
    path('', getAllNotes, name='list_view'),
    path('create', createNotes, name='view_notes'),
    path('<id>', getNotes, name='detail_notes'),
    path('<id>/update', updateNotes, name='update_notes'),
    path('<id>/delete', deleteNotes, name='delete_notes')
]