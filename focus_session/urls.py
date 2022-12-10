from django.urls import path
from focus_session.views import *

urlpatterns = [
    path('focus/', timer, name='focus_session'),

]