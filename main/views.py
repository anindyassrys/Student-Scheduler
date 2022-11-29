from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .models import Question,Answer
from django.core.paginator import Paginator
from .forms import AnswerForm, QuestionForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'home.html')

def QnA(request):
    q=Question.objects.all().order_by('-id')
    paginator=Paginator(q,5)
    page_num = request.GET.get('page',1)
    q=paginator.page(page_num)
    return render(request, 'Q&A.html',{'q':q})

def detail(request,id):
    q=Question.objects.get(pk=id)
    try:
      answer = Answer.objects.get(question=q)
      return render(request,'detail.html',{'q':q,'answer':answer})
    except Answer.DoesNotExist:
        return render(request,'belum.html',{'q':q})
    


@user_passes_test(lambda u: u.is_staff)
def answerForm(request,id):
    q=Question.objects.get(pk=id)
    # answer=Answer.objects.get(question=q)
    answer='x'
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=q
            answer.save()
            return redirect('/QnA')
            messages.success(request,'Answer has been submitted.')
    return render(request,'formAnswer.html',{'q':q,'answer':answer,'answerform':answerform})

def questionForm(request):
    # q=Question.objects.get(pk=id)
    # answer=Answer.objects.get(question=q)
    q='x'
    questionform=QuestionForm
    if request.method=='POST':
        qData=QuestionForm(request.POST)
        if qData.is_valid():
            q=qData.save(commit=False)
            q.user=request.user
            q.save()
            return redirect('/QnA')
            messages.success(request,'Question has been submitted.')
    return render(request,'formQuestion.html',{'q':q,'questionform':questionform})

    # User Register
def register(request):
    form=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'User has been registered!!')
    return render(request,'registration/register.html',{'form':form})

    from django.contrib.auth.decorators import user_passes_test