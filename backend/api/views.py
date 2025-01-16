from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, AccountSerializer, CategorySerializer, EntrySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account, Category, Entry


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
        user = self.request.user
        return Entry.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class EntryDelete(generics.DestroyAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]