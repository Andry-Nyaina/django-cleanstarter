from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Bienvenue sur Django CleanStarter 🚀")
