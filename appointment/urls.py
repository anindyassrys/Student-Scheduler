from django.urls import path
from .views import *

urlpatterns = [
    path('', get_appointments, name='appointments'),
    path('create', create_appointment, name='create_appointment'),
    path('get/<id>', get_appointment_detail, name='appointment_detail'),
    path('accept/<id>', accept_appointment, name='accept_appointment'),
    path('reject/<id>', reject_appointment, name='reject_appointment'),
]