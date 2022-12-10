from django.shortcuts import render
from .models import *

# Create your views here.
def timer(request):
  # ob=chek.objects.all()
  return render(request,'timer.html')