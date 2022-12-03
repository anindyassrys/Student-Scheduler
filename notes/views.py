from django.shortcuts import render
from .models import Notes
from .forms import NotesForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from todo_list.models import *
from django.http import Http404
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def get_notes(request):
    current_user = Pengguna.objects.get(id=request.user.id)
    response = {
        'notes': current_user.getAllNotesUser().order_by('title').all().values()
        }
    return render(request, 'view_notes.html', response)

@login_required
def get_detail_notes(request, id):
    current_user: Pengguna = Pengguna.objects.get(id=request.user.id)

    fetched_notes = current_user.getNotes(id)
    if fetched_notes != None:
        response = {
            'notes_list': fetched_notes
        }
        return render(request, 'detail_notes.html', response)
    else:
        raise Http404("Notes does not exist")

@csrf_exempt
@login_required
def create_notes(request):
    if request.method=='GET':
        data = list(Pengguna.objects.values())
        return JsonResponse(data, safe=False)
        #return render(request, 'create_notes.html')

    elif request.method=='POST':
        current_user: Pengguna = Pengguna.objects.get(id=request.user.id)
        parsed_body = json.loads(request.body)
        current_user.createNotes(parsed_body['notes_title'], parsed_body['notes_description'])
        
    return render(request, 'view_notes.html')

@login_required
def delete_notes(request, id):
    current_user: Pengguna = Pengguna.objects.get(id=request.user.id)
    fetched_notes:Notes = current_user.getNotes(id)
    if fetched_notes == None:
        raise Http404("Notes does not exist")
    else:
        current_user.deleteNotes(fetched_notes.id)
    return render(request, 'view_notes.html')
