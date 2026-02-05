# views.py

from django.http import HttpResponse, JsonResponse

def home(request):
   return HttpResponse("<h1> Hello this is my home page </h1>")

def home1(request):
   return HttpResponse("This is my Job Tracker API")
