from rest_framework import serializers
from decimal import Decimal
from service.models import Category, Service,Review,ServiceImage
from django.contrib.auth import get_user_model


class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(method_name='get_user')
    # average_rating = serializers.SerializerMethodField(method_name='get_average_rating')
    class Meta:
        model=Review
        fields=['id','user','comment','ratings']
        read_only_fields = ['user']
    
    # def get_average_rating(self, obj):
    #     average = Review.objects.filter(service=obj.service).aggregate(avg_rating=Avg('ratings'))['avg_rating']
    #     return round(average, 2) if average else 0.0
    
    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self, validated_data):
        service_id = self.context['service_id']
        review = Review.objects.create(service_id=service_id, **validated_data)
        return review

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'service_count']
        
    service_count = serializers.IntegerField(read_only=True)


class ServiceSerializer(serializers.ModelSerializer):
    images=ServiceImageSerializer(many=True,read_only=True)
    # average_rating= ReviewSerializer(many=True,read_only=True)
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating')
    total_review = serializers.SerializerMethodField(method_name='get_review_count')
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price_per_piece',
                  'max_quantity', 'category', 'images','available','price_with_tax','average_rating','total_review']  
    
    def get_review_count(self, service):
        return service.reviews.count()
        # return service.review_set.count()
    
    def get_average_rating(self, service):
        average = getattr(service, 'average_rating', None)
        return round(average, 2) if average else 0.0
    
    # def get_average_rating(self, service):
    #     average = service.reviews.aggregate(avg=Avg('ratings'))['avg']
    #     return round(average, 2) if average else 0.0
    
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, service):
        return round(service.price_per_piece * Decimal(1.1), 2)

    # def validate_price(self, price):
    #     if price < 0:
    #         raise serializers.ValidationError('Price could not be negative')
    #     return price
class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields =['id','name']
    def get_current_user_name(self,obj):
        return obj.get_full_name()

