from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'staff'),}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')
    list_display_links = ('id', 'username')


admin.site.register(Users, UserAdmin)

admin.site.register(Categories)



@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price', 'discount', 'description')
    list_display_links = ('id', 'category')


@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'total', 'status', 'date')
    list_display_links = ('id', 'client')
    list_filter = ('status',)
    date_hierarchy = 'date'


@admin.register(ShopItems)
class ShopItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'quantity', 'total')
    list_display_links = ('id', 'shop')