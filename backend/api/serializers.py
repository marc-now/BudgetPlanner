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
    # ID for POST/PUT purposes
    account_id = serializers.PrimaryKeyRelatedField(
        source='account',
        queryset=Account.objects.all(),
        write_only=True
    )   
    # Whole data for GET purposes
    account = AccountSerializer(read_only=True)

    # Names for simplicity of POST/PUT
    # Whole serializers for GETS to avoid N+1
    category_name = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    subcategory_name = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
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

    def validate(self, attrs):
        request_user = self.context["request"].user
        account = attrs.get("account")

        if account and account.user != request_user:
            raise serializers.ValidationError("Selected Account does not belong to the authenticated User!")

        return attrs

    def create(self, validated_data):
        category_name = validated_data.pop("category_name", None)
        subcategory_name = validated_data.pop("subcategory_name", None)

        category = None
        subcategory = None

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            if subcategory_name:
                subcategory, _ = Subcategory.objects.get_or_create(name=subcategory_name, category=category)

        return Entry.objects.create(
            **validated_data,
            category=category,
            subcategory=subcategory
        )

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category_name", None)
        subcategory_name = validated_data.pop("subcategory_name", None)

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            instance.category = category
            if subcategory_name:
                subcategory, _ = Subcategory.objects.get_or_create(name=subcategory_name, category=category)
                instance.subcategory = subcategory
            elif subcategory_name == None:
                instance.subcategory = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance