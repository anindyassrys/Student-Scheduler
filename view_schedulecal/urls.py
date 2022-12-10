from django.urls import path
from .views import *

urlpatterns = [
    path('schedule/', listEvent, name='schedule'),
    path('schedule/create-event', createEvent, name='create_schedule'),
    path('schedule/detail/<id>', detail, name='detail_schedule'),
    path('schedule/detail/event/<id>', detailEvent, name='detail_schedule_event'),

]