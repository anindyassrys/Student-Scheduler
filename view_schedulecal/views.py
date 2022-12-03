from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .models import Event
from django.core.paginator import Paginator
# from .forms import AnswerForm, QuestionForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test


def home(request):
    return render(request, 'home.html')

def listEvent(request):
    q=Event.objects.all().order_by('-id')
    paginator=Paginator(q,5)
    page_num = request.GET.get('page',1)
    q=paginator.page(page_num)
    return render(request, 'listEvent.html',{'q':q})

def detail(request,id):
    q=Event.objects.get(pk=id)
    return render(request,'detailEvent.html',{'q':q,'detail':detail})


