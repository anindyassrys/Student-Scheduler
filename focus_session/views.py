from django.shortcuts import render
from .models import *

# Create your views here.
def jaya(request):
  ob=chek.objects.get(id=2)
  return render(request,'jaya.html',{'ob':ob})