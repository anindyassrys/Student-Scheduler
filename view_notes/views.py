from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notes
from .forms import NotesForm
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
 
@login_required
def getAllNotes(request):
    context ={}
    context["dataset"] = Notes.objects.all()        
    return render(request, "notes_view.html", context)

@login_required
def createNotes(request):
	context ={}

	form = NotesForm(request.POST or None)
	if form.is_valid():
		form.save()	
        
	context['form']= form
	return render(request, "notes_create.html", context)

@login_required
def getNotes(request, id):
    context ={}
    context["data"] = Notes.objects.get(id = id)    
    return render(request, "detail_notes.html", context)

@login_required
def updateNotes(request, id):
    context ={}
    obj = get_object_or_404(Notes, id = id)

    form = NotesForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/view-notes/"+id)
    context["form"] = form

    return render(request, "update_notes.html", context)

@login_required
def deleteNotes(request, id):
    context ={}
    obj = get_object_or_404(Notes, id = id)
 
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/view-notes")
 
    return render(request, "delete_notes.html", context)
