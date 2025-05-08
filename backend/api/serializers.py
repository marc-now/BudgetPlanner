from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Account, Category, Entry, Subcategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "user", "name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]

class EntrySerializer(serializers.ModelSerializer):
    # ID for POST purposes
    account_id = serializers.PrimaryKeyRelatedField(
        source='account',
        queryset=Account.objects.all(),
        write_only=True
    )   
    # Whole data for GET purposes
    account = AccountSerializer(read_only=True)

    # Names for simplicity of POST
    # Whole serializers for GETS to avoid N+1
    category_name = serializers.CharField(write_only=True)
    subcategory_name = serializers.CharField(write_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)

    class Meta:
        model = Entry
        fields = [
            "id", "title", "value", "description", "date",
            "account", "account_id",
            "category", "category_name",
            "subcategory", "subcategory_name",
        ]
