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
    def by_client(self, request):
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