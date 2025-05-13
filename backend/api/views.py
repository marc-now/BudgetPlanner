from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from .serializers import UserSerializer, AccountSerializer, CategorySerializer, EntrySerializer, SubcategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account, Category, Entry, Subcategory


class AccountListCreate(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class AccountDelete(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)

class EntryListCreate(generics.ListCreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # We check Account object in the given Entry
        # in the Account, we check the User
        # if the User matches the User in request, we return the Entry
        return Entry.objects.filter(account__user=self.request.user).select_related(
            "account", "category", "subcategory" # All 3 are just IDs (FKs) in the Model, but select_related returns whole objects
        )

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()


class EntryDelete(generics.DestroyAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Entry.objects.filter(account__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Save data before deleting so it can be returned in response properly
        serializer_data = self.get_serializer(instance).data
        self.perform_destroy(instance)
        return Response(serializer_data, status=status.HTTP_200_OK)

class EntryUpdate(generics.UpdateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Entry.objects.filter(account__user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer= self.get_serializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response({"message":"failed"})


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Account.objects.create(name="default", user=user)