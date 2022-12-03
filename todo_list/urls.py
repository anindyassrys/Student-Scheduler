from django.urls import path
from todo_list.views import *

urlpatterns = [
    path('todo-lists', get_todo_lists, name='todo_lists'),
    path('todo-list/<id>', get_detail_todo_list, name='detail_todo_list'),
    path('todo-list/<id>/update', update_todo_list, name='update_todo_list'),
    path('todo-list/<id>/delete', delete_todo_list, name='delete_todo_list'),
    path('todo-lists/create', create_todo_list, name='create_todo_list'),
]