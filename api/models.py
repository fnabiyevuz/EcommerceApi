from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    sts = (
        ("client", "client"),
        ("call_center", "call_center"),
        ("manager", "manager"),
        ("deliver", "deliver"),
        ("cashier", "cashier"),
    )
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Categories(models.Model):
    image = models.ImageField(upload_to='category')
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='prod_cat')
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.name
    

class Shops(models.Model):
    sts = (
        ("opened", "opened"),
        ("booked", "booked"),
        ("canceled", "canceled"),
        ("accepted", "accepted"),
        ("sent", "sent"),
        ("sold", "sold"),
        ("paid", "paid"),
    )
    client = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='shop_user')
    total = models.FloatField(default=0)
    status = models.CharField(choices=sts, max_length=10, default='opened')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class ShopItems(models.Model):
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, related_name='shop_item')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='prod_item')
    quantity = models.IntegerField(default=1)
    total = models.FloatField()

    def __str__(self):
        return str(self.id)