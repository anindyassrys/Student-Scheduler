from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

from .models import AppointmentRequest

@login_required
def get_appointments(request):
    sent = AppointmentRequest.objects.getSentAppointmentRequests(request.user)
    received = AppointmentRequest.objects.getReceivedAppointmentRequests(request.user)
    response = {
        'sent': sent,
        'received': received
    }
    # return render(request, 'appointments.html', response)
    return HttpResponse(AppointmentRequest.objects.values())

@login_required
def get_appointment_detail(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        response = {
            'appointment': appointment
        }
        # return render(request, 'appointment_detail.html', response)
        return HttpResponse(appointment.isAccepted)
    except:
        raise Http404("Appointment not found")

@login_required
def accept_appointment(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        appointment.isAccepted = True
        appointment.save()
        # return render(request, 'appointments.html')
        return HttpResponse('Accepted')
    except:
        raise Http404("Appointment not found")

@login_required
def reject_appointment(request, id):
    try:
        appointment = AppointmentRequest.objects.get(pk=id)
        appointment.isAccepted = False
        appointment.save()
        # return render(request, 'appointments.html')
        return HttpResponse('Rejected')
    except:
        raise Http404("Appointment not found")

@login_required
def create_appointment(request):
    if request.method == 'GET':
        return render(request, 'create_appointment.html')

    elif request.method == 'POST':
        sender = request.user
        parsed_body = json.loads(request.body)
        receiver = User.objects.get(pk=parsed_body['receiver_id'])
        datetime =  parsed_body['datetime']
        description =  parsed_body['description']
        AppointmentRequest.objects.create(sender=sender,receiver=receiver,datetime=datetime,description=description)

    return render(request, 'appointments.html')
