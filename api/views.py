from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Product
from .serializers import ProductSerializer, RegisterSerializer
from .utils import success_response, error_response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from core.permissions import *
from .serializers import RegisterSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return success_response(ProductSerializer(product).data, "Produit créé avec succès", status=201)
        return error_response(serializer.errors, status=400)
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            product = serializer.save()
            return success_response(
                ProductSerializer(product).data,
                "Produit mis à jour avec succès",
                status=200
            )

        return error_response(serializer.errors, status=400)
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data, "Liste des produits", status=200)
    

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return success_response(serializer.data, "Produit récupéré avec succès")
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message="Produit supprimé avec succès", status=204)

    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Utilisateur enregistré avec succès", status=201)
        return error_response(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUserOnly]

    def get_permissions(self):
        # GET /api/users/ (liste)
        if self.action == "list":
            return [IsAdmin()]

        # GET /api/users/ID/
        if self.action == "retrieve":
            return [IsAdminOrSelf()]

        # PUT / PATCH : modifier un user
        if self.action in ["update", "partial_update"]:
            return [IsAdminOrSelf()]

        # DELETE
        if self.action == "destroy":
            return [IsAdmin(), DenyDeleteSelf()]

        # POST /api/users/ (création depuis viewset si activé)
        return [IsAdmin()]

