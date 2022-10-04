from rest_framework.routers import DefaultRouter
from .viewsets import *

router = DefaultRouter()
router.register('user', UsersViewset)
router.register('categories', CategoriesViewset)
router.register('products', ProductsViewset)
router.register('shops', ShopsViewset)
router.register('shopitems', ShopItemsViewset)