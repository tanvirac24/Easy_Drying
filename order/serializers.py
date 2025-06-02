from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from service.models import Service
from service.serializers import ServiceSerializer
from rest_framework.permissions import IsAuthenticated
from order.services import OrderService



class EmptySerializer(serializers.Serializer):
    pass



class SimpleserviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price_per_piece']

class AddCartItemSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'service_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        service_id = self.validated_data['service_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, service_id=service_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance
       #(Checking The id exist or not)
    def validate_service_id(self, value):
        if not Service.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Bro, Service with id- {value} does not exists!")
        return value
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']     


class CartItemSerializer(serializers.ModelSerializer):
    service = SimpleserviceSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'service', 'quantity','total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.service.price_per_piece

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user','items','total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum(
            [item.service.price_per_piece * item.quantity for item in cart.items.all()])
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No Cart is found with this id, Bro!')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is Empty, Bro!')
        return cart_id
    def create(self,validated_data):
        user_id=self.context['user_id']
        cart_id = validated_data['cart_id']
        try:
            order = OrderService.create_order(user_id=user_id,cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    
class OrderItemSerializer(serializers.ModelSerializer):
    service = SimpleserviceSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'service','total_price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']
        read_only_fields=['user','items']
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
    # def update(self, instance, validated_data):
    #     user = self.context['user']
    #     new_status = validated_data['status']

    #     if new_status == Order.CANCELED:
    #         return OrderService.cancel_order(order=instance,user=user)

    #     if not user.is_staff:
    #         raise serializers.ValidationError({'detail':'You are not allowed to update this order'})
    #     # instance.status = new_status
    #     # instance.save()
    #     # return instance
    #     return super().update(instance, validated_data)




















# from rest_framework import serializers
# from order.models import Cart, CartItem, Order, OrderItem
# from service.models import Service
# from service.serializers import ServiceSerializer
# from order.services import OrderService


# class EmptySerializer(serializers.Serializer):
#     pass


# class SimpleserviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = ['id', 'name', 'price']


# class AddCartItemSerializer(serializers.ModelSerializer):
#     service_id = serializers.IntegerField()

#     class Meta:
#         model = CartItem
#         fields = ['id', 'service_id', 'quantity']

#     def save(self, **kwargs):
#         cart_id = self.context['cart_id']
#         service_id = self.validated_data['service_id']
#         quantity = self.validated_data['quantity']

#         try:
#             cart_item = CartItem.objects.get(
#                 cart_id=cart_id, service_id=service_id)
#             cart_item.quantity += quantity
#             self.instance = cart_item.save()
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(
#                 cart_id=cart_id, **self.validated_data)

#         return self.instance

#     def validate_service_id(self, value):
#         if not Service.objects.filter(pk=value).exists():
#             raise serializers.ValidationError(
#                 f"service with id {value} does not exists")
#         return value


# class UpdateCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['quantity']


# class CartItemSerializer(serializers.ModelSerializer):
#     service = SimpleserviceSerializer()
#     total_price = serializers.SerializerMethodField(
#         method_name='get_total_price')

#     class Meta:
#         model = CartItem
#         fields = ['id', 'service', 'quantity', 'service', 'total_price']

#     def get_total_price(self, cart_item: CartItem):
#         return cart_item.quantity * cart_item.service.price


# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#     total_price = serializers.SerializerMethodField(
#         method_name='get_total_price')

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items', 'total_price']
#         read_only_fields = ['user']

#     def get_total_price(self, cart: Cart):
#         return sum(
#             [item.service.price * item.quantity for item in cart.items.all()])


# class CreateOrderSerializer(serializers.Serializer):
#     cart_id = serializers.UUIDField()

#     def validate_cart_id(self, cart_id):
#         if not Cart.objects.filter(pk=cart_id).exists():
#             raise serializers.ValidationError('No cart found with this id')

#         if not CartItem.objects.filter(cart_id=cart_id).exists():
#             raise serializers.ValidationError('Cart is empty')

#         return cart_id

#     def create(self, validated_data):
#         user_id = self.context['user_id']
#         cart_id = validated_data['cart_id']

#         try:
#             order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
#             return order
#         except ValueError as e:
#             raise serializers.ValidationError(str(e))

#     def to_representation(self, instance):
#         return OrderSerializer(instance).data


# class OrderItemSerializer(serializers.ModelSerializer):
#     service = SimpleserviceSerializer()

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'service', 'price', 'quantity', 'total_price']


# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['status']


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']