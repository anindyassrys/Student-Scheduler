from . import views
from django.urls import path,include

from main.views import *

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('QnA', QnA ,name='QnA'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('qform',views.questionForm,name='questionForm'),
    path('answerForm/<int:id>',views.answerForm,name='answerForm'),
    # User Register
    path('accounts/register/',views.register,name='register'),
]