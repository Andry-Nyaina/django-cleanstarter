from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Product
from .serializers import ProductSerializer, RegisterSerializer
from .utils import success_response, error_response
from django.contrib.auth.models import User

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return success_response(ProductSerializer(product).data, "Produit créé avec succès", status=201)
        return error_response(serializer.errors, status=400)
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Utilisateur enregistré avec succès", status=201)
        return error_response(serializer.errors, status=400)
