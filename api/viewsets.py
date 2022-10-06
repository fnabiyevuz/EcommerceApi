from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from django.db.models import Q

class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            dt = self.get_serializer_class()(user).data
            return Response({'result':dt})
        else:
            return Response({'result': 'user is not registered'})

    
    @action(methods=['post'], detail=False)
    def register(self, request):
        username = request.data['username']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        birthday = request.data['birthday']
        phone = request.data['phone']
        staff = request.data['staff']
        address = request.data['address']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'result': f'{username} already taken!'})
        else:
            user = Users.objects.create(username=username, password=make_password(password), first_name=first_name, last_name=last_name, birthday=birthday, phone=phone, staff=staff, address=address)
            dt = self.get_serializer_class()(user).data
            return Response({'result':dt})

    def create(self, request):
        return Response({"detail": "Method \'POST\' not allowed."})

    def destroy(self, request, pk=None):
        return Response({"detail": "Method \'DELETE\' not allowed."})

    @action(methods=['get'], detail=False)
    def by_staff(self, request):
        st = request.GET['st']
        data = Users.objects.filter(staff=st)
        dt = self.get_serializer_class()(data, many=True).data
        
        return Response({'result':dt})


class CategoriesViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ProductsViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


    @action(methods=['get'], detail=False)
    def by_cat(self, request):
        cat = request.GET['cat']
        data = Products.objects.filter(category_id=cat)
        dt = self.get_serializer_class()(data, many=True).data
        return Response({'result':dt})


    @action(methods=['get'], detail=False)
    def discount(self, request):
        data = Products.objects.filter(~Q(discount=None))
        dt = self.get_serializer_class()(data, many=True).data
        
        return Response({'result':dt})



class ShopsViewset(viewsets.ModelViewSet):
    queryset = Shops.objects.all()
    serializer_class = ShopsSerializer

    @action(methods=['get'], detail=False)
    def by_client_and_status(self, request):
        cli = request.data['cli']
        try:
            sts = request.data['sts']
            data = Shops.objects.filter(client_id=cli, status=sts)
        except:
            data = Shops.objects.filter(client_id=cli)
        dt = self.get_serializer_class()(data, many=True).data
        
        return Response({'result':dt})

class ShopItemsViewset(viewsets.ModelViewSet):
    queryset = ShopItems.objects.all()
    serializer_class = ShopItemsSerializer
    
    @action(methods=['post'], detail=False)
    def add(self, request):
        client = request.data['client']
        items = request.data['items']
        try:
            shp = Shops.objects.get(client_id=client, status='opened')
        except:
            shp = Shops.objects.create(client_id=client, status='opened')
        
        for i in items:
            prod = Products.objects.get(id=i['product'])
            if prod.discount:
                price = prod.discount
            else:
                price = prod.price
            ShopItems.objects.create(shop=shp, product=i['product'], quantity=i['quantity'], total=price*int(i['quantity']))
            shp.total += price*int(i['quantity'])
        shp.save()


    @action(methods=['post'], detail=False)
    def add_one_by_one(self, request):
        client = request.data['client']
        product = request.data['product']
        quantity = int(request.data['quantity'])
        try:
            shp = Shops.objects.get(client_id=client, status='opened')
        except:
            shp = Shops.objects.create(client_id=client, status='opened')
        prod = Products.objects.get(id=product)
        if prod.discount:
            price = prod.discount
        else:
            price = prod.price
        items = shp.shop_item.all()
        result = False
        for i in items:
            if i.product == prod:
                item = i
                result = True
                break
        if result:
            item.quantity += quantity
            item.total += price * quantity
            item.save()
        else:
            item = ShopItems.objects.create(shop=shp, product=prod, quantity=quantity, total=price*quantity)
        shp.total += price*quantity
        shp.save()

        dt = self.get_serializer_class()(item).data

        return Response(dt)


    @action(methods=['post'], detail=False)
    def delete_item(self, request):
        item = request.data['item']

        item = ShopItems.objects.get(id=item)
        shop = item.shop
        shop.total -= item.total
        shop.save()
        item.delete()

        dt = ShopsSerializer(shop).data

        return Response(dt)