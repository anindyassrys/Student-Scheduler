from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from todo_list.models import *
from django.http import Http404, JsonResponse
import json

@login_required
def get_todo_lists(request):
    current_user:Pengguna = Pengguna.objects.get(id=request.user.id)
    # if(len(current_user.getAllTodoList()) == 0):
    #     current_user.createTodoList("list1", ["todo1", "todo2"])
    #     current_user.createTodoList("list2", ["todo1", "todo2"])
    response = {
        'todo_lists': current_user.getAllTodoList().order_by('name').all().values()
        }
    return render(request, 'todo_lists.html', response)

@login_required
def get_detail_todo_list(request, id):
    current_user: Pengguna = Pengguna.objects.get(id=request.user.id)

    fetched_todo_list = current_user.getTodoList(id)
    if fetched_todo_list != None:
        response = {
            'todo_list': fetched_todo_list
        }
        return render(request, 'todo_list_detail.html', response)
    else:
        raise Http404("Todo List does not exist")

@login_required
def update_todo_list(request, id):
    current_user: Pengguna = Pengguna.objects.get(id=request.user.id)
    fetched_todo_list:ToDoList = current_user.getTodoList(id)
    if request.method=='POST':
    
        if fetched_todo_list == None:
            raise Http404("Todo List does not exist")
        else:
            parsed_req = json.loads(request.body)
            todo_ids = parsed_req['todos']
            new_name = parsed_req['new_name']
            print(new_name)
            fetched_todo_list.name = new_name
            fetched_todo_list.markDone(todo_ids)
            fetched_todo_list.save()
        return JsonResponse({})

    if fetched_todo_list != None:
        response = {
            'todo_list': fetched_todo_list
        }
        return render(request, 'update_todo_list.html', response)
    else:
        raise Http404("Todo List does not exist")

@login_required
def create_todo_list(request):
    if request.method=='GET':
        return render(request, 'create_todo_list.html')

    elif request.method=='POST':
        current_user: Pengguna = Pengguna.objects.get(id=request.user.id)
        parsed_body = json.loads(request.body)
        current_user.createTodoList(parsed_body['list_name'], parsed_body['todo_names'])
        return JsonResponse({})    
    

@login_required
def delete_todo_list(request, id):
    current_user: Pengguna = Pengguna.objects.get(id=request.user.id)
    fetched_todo_list:ToDoList = current_user.getTodoList(id)
    if fetched_todo_list == None:
        raise Http404("Todo List does not exist")
    else:
        current_user.deleteTodoList(fetched_todo_list.id)
    response = {
            'todo_lists': current_user.getAllTodoList() 
        }
    return redirect('todo_lists')