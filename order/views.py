from django.shortcuts import render
from order import serializers as OrderE
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from order.serializers import UpdateOrderSerializer,CreateOrderSerializer,OrderSerializer,UpdateCartItemSerializer,AddCartItemSerializer,CartSerializer,CartItemSerializer
from order.models import Cart,CartItem, Order, OrderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin, RetrieveModelMixin
from order.services import OrderService
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
# Create your views here.

class CartViewSet(CreateModelMixin,GenericViewSet, DestroyModelMixin,RetrieveModelMixin):
    """
    API endpoints for managing carts in the E-comerce site
    - Allow Only authenticated user(clients) to change own carts
    - Support proper pagination system
    - Allow any user(clients) to show own carts
    - Admin has a control of changing everything
    """
    # queryset = Cart.objects.all()
    serializer_class= CartSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.filter(user=self.request.user)
    
    def create(self,request,*args,**kwargs):
        existing_cart= Cart.objects.filter(user=request.user).first()

        if existing_cart:
            serializer=self.get_serializer(existing_cart)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return super().create(request,*args,**kwargs)
class CartItemViewSet(ModelViewSet):
    """
    API endpoints for managing carts in the E-comerce site
    - Allow Only authenticated user(clients) to change own carts
    - Support proper pagination system
    - Allow any user(clients) to show own carts
    - Admin has a control of changing everything
    """
    http_method_names=['get','post','patch','delete']
    # serializer_class= CartItemSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))


class OrderViewSet(ModelViewSet):
    """
    API endpoints for managing orders in the E-comerce site
    - Allow Only authenticated user(clients) to change own orders(only Canceling option)
    - Support proper pagination system
    - Allow any user(clients) to show own orders
    - Admin has a control of changing everything
    - User's(clients) carts will be deleted after creating it's order !
    """
    # queryset =Order.objects.all()
    # serializer_class = OrderSerializer
    permission_class =[IsAuthenticated]
    http_method_names=['get','post','delete','head','options','patch']
    
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
    def  cancel(self,request,pk=None):
        order= self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status':'Order canceled!'})
    
    @action(detail=True,methods=['patch'],permission_classes=[IsAdminUser])
    def update_status(self,request,pk=None):
        order= self.get_object()
        serializer=UpdateOrderSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order status updated to {request.data['status']}'})

    # def get_permissions(self):
    #     if self.action in ['update_status','destroy']:
    #         return[IsAdminUser()]
    #     return [IsAuthenticated()]
    def get_permissions(self):
        if self.request.method in ['DELETE','PATCH']:
            return[IsAdminUser()]
        return [IsAuthenticated()]
    
    #(Module ------ 24.9)
    def get_serializer_class(self):
        if self.action =='cancel':
            return OrderE.EmptySerializer
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method =='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id, 'user': self.request.user}
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__service').all()
        return Order.objects.prefetch_related('items__service').filter(user=self.request.user)