from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def home(request):
    #return HttpResponse("Bienvenue sur Django CleanStarter 🚀")
    return render(request, "core/home.html")



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]