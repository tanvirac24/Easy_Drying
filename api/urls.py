from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from service.views import ServiceImageViewSet,ServiceViewSet,CategoryViewSet,ReviewViewSet
from users.views import UpdateStatusUserViewSet
from rest_framework_nested import routers
from order.views import OrderViewSet,CartViewSet,CartItemViewSet


router= routers.DefaultRouter()
router.register('services',ServiceViewSet,basename='services')
router.register('category', CategoryViewSet)
router.register('carts', CartViewSet,basename='carts')
router.register('orders',OrderViewSet,basename='orders')
router.register('staus_update',UpdateStatusUserViewSet,basename='status-update')

service_router = routers.NestedDefaultRouter(router,'services',lookup='service')
service_router.register('reviews',ReviewViewSet,basename='service-review')
service_router.register('images',ServiceImageViewSet,basename='service-images')
cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')
urlpatterns=[
    path('',include(router.urls)),
    path('',include(service_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]