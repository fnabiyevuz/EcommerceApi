from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'birthday', 'phone', 'staff', 'address']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = '__all__'


class ShopItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItems
        fields = '__all__'