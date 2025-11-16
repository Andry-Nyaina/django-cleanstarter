from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Product
from .serializers import ProductSerializer, RegisterSerializer
from .utils import success_response, error_response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from core.permissions import IsAdmin, IsSelf, IsAdminOrSelf, DenyDeleteSelf
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
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Utilisateur enregistré avec succès", status=201)
        return error_response(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        # GET /api/users/ (liste)
        if self.action == "list":
            return [IsAdmin()]

        # GET /api/users/ID/
        if self.action == "retrieve":
            return [IsAdminOrSelf()]

        # PUT / PATCH : modifier un user
        if self.action in ["update", "partial_update"]:
            return [IsSelf()]

        # DELETE
        if self.action == "destroy":
            return [IsAdmin(), DenyDeleteSelf()]

        # POST /api/users/ (création depuis viewset si activé)
        return [IsAdmin()]

