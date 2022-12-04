from django.shortcuts import redirect, render
from .models import Event
from .forms import EventForm
from appointment.models import AppointmentRequest
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def listEvent(request):
    q=AppointmentRequest.objects.getAcceptedAppointmentRequests(request.user)
    e=Event.objects.all()
    return render(request, 'listEvent.html',{'q':q,'e':e})

def detail(request,id):
    q=AppointmentRequest.objects.getAcceptedAppointmentRequests(request.user).get(pk=id)
    return render(request,'detailEvent.html',{'q':q})

@login_required
def createEvent(request):
    context={}
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request,"createEvent.html",context)

