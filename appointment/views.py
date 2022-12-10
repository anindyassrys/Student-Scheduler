from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import AppointmentRequest

@login_required
def get_appointments(request):
    sent = AppointmentRequest.objects.getSentAppointmentRequests(request.user)
    received = AppointmentRequest.objects.getReceivedAppointmentRequests(request.user)
    response = {
        'sent': sent,
        'received': received
    }
    return render(request, 'appointments.html', response)

@login_required
def get_appointment_detail(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        response = {
            'appointment': appointment
        }
        return render(request, 'appointment_detail.html', response)
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('appointments')

@login_required
def accept_appointment(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        appointment.isAccepted = True
        appointment.save()
        return redirect('appointments')
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('appointment_detail', id=id)

@login_required
def reject_appointment(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        appointment.isAccepted = False
        appointment.save()
        return redirect('appointments')
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('appointment_detail', id=id)

@login_required
def create_appointment(request):
    if request.method == 'GET':
        users = User.objects.exclude(pk=request.user.id)
        response = {
            'users': users
        }
        return render(request, 'create_appointment.html', response)

    elif request.method == 'POST':
        try:
            sender = request.user
            receiver = User.objects.get(pk=request.POST['receiver'])
            datetime = request.POST['datetime']
            description = request.POST['description']
            AppointmentRequest.objects.create(sender=sender,receiver=receiver,datetime=datetime,description=description)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return redirect('create_appointment')
        
    return redirect('appointments')
