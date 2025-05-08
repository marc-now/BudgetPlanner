from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, serializers
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

    def perform_create(self, serializer):
        account = serializer.validated_data["account"]
        if account.user != self.request.user:
            raise serializers.ValidationError("Selected Account does not belong to the authenticated User!")

        category_name = serializer.validated_data.pop("category_name")
        subcategory_name = serializer.validated_data.pop("subcategory_name")

        category, _ = Category.objects.get_or_create(name=category_name)
        subcategory, _ = Subcategory.objects.get_or_create(name=subcategory_name, category=category)

        serializer.save(category=category, subcategory=subcategory)

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()


class EntryDelete(generics.DestroyAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Entry.objects.filter(account__user=self.request.user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Account.objects.create(name="default", user=user)