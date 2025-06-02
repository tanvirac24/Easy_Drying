from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from service.models import Service, Category,Review,ServiceImage
from service.serializers import ServiceImageSerializer,ReviewSerializer,ServiceSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from service.filters import ServiceFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser,AllowAny
from api.permissions import IsAdminOrReadOnly,FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions
from service.permissions import IsReviewAuthorReadonly
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Avg
# Create your views here.

class ServiceViewSet(ModelViewSet):
    """
    API endpoints for managing services in the E-comerce site
    - Allow Only authenticated(admin) to change any change
    - Offer filter feature(Ascending & Descending Price and also updated perspectives,Based on Category)
    - Support proper pagination system
    - Allow Search operation on(name,category_name & both description) fields
    - Allow any user(clients/admin) to show all services
    """
    queryset= Service.objects.all()
    serializer_class= ServiceSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields= ['category_id']
    filterset_class = ServiceFilter
    # pagination_class= PageNumberPagination
    search_fields=['name','category__name','description']
    ordering_fields=['price_per_piece','updated_at','average_rating']
    permission_classes=[FullDjangoModelPermission]
    def get_queryset(self):
        return Service.objects.annotate(average_rating=Avg('reviews__ratings'))







    @swagger_auto_schema(
            operation_summary='Retrieve All Services by(Admin/clients)'
    )
    def list(self, request, *args, **kwargs):
        """Retrieve All Services"""
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Allow Creating by Admin'
    )
    def create(self, request, *args, **kwargs):
        """Only Admin Can perform this action"""
        return super().create(request, *args, **kwargs)
    #(module - 25.6)
    @swagger_auto_schema(
            operation_summary='Allow Deleting by Admin',
            operation_description='Admin Can prform this action'
    )
    def destroy(self, request, *args, **kwargs):
        """Only admin can perform this action"""
        return super().destroy(request, *args, **kwargs)
class ServiceImageViewSet(ModelViewSet):
    """
    API endpoints for managing service_images in the E-comerce site
    - Allow Only authenticated(admin) to change any change
    - Support proper pagination system
    - Allow Multiple uploads(individual_size< 10MB)
    - Allow any user(clients/admin) to show all 
    """  
       
    serializer_class=ServiceImageSerializer
    permission_classes=[IsAdminUser]
    def get_queryset(self):
        return ServiceImage.objects.filter(service_id=self.kwargs.get('service_pk'))
    def perform_create(self, serializer):
        serializer.save(service_id=self.kwargs.get('service_pk'))
        

    # def get_queryset(self):
    #     queryset = Service.objects.all()
    #     category_id= self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset = Service.objects.filter(category_id=category_id)
    #     return queryset

    
    
    # def destroy(self, request, *args, **kwargs):
    #     service=self.get_object()
    #     if service.max_quantity>10:
    #         return Response({"message": "Product with stock more than 10 could not be deleted"})
    #     self.perform_destroy(service)
    #     return Response(status=status.HTTP_201_CREATED)
    def list(self, request, *args, **kwargs):
        """Retrieve All Services"""
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        """Only Admin Can perform this action"""
        return super().create(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        """Only admin can perform this action"""
        return super().destroy(request, *args, **kwargs)
    

class CategoryViewSet(ModelViewSet):
    """
    API endpoints for managing categories in the E-comerce site
    - Allow Only authenticated(admin) to change any change
    - Don't Offer filter feature & Search operation 
    - Support proper pagination system
    - Allow any user(clients/admin) to show all categories
    """
    permission_classes =[FullDjangoModelPermission]
    queryset= Category.objects.annotate(service_count=Count('services')).all()
    serializer_class= CategorySerializer

    def list(self, request, *args, **kwargs):
        """Retrieve All Services"""
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        """Only Admin Can perform this action"""
        return super().create(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        """Only admin can perform this action"""
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    """
    API endpoints for managing reviews in the E-comerce site
    - Allow Only authenticated(admin) to access all reviews
    - Clients can access only their own reviews
    - Support proper pagination system
    - Allow any user(clients/admin) to show all reviews
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorReadonly]
    filter_backends=[OrderingFilter]
    ordering_fields=['ratings']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(service_id=self.kwargs.get('service_pk'))

    def get_serializer_context(self):
        return {'service_id': self.kwargs.get('service_pk')}
    

    # serializer_class=ReviewSerializer
    # def get_queryset(self):
    #     return Review.objects.filter(service_id=self.kwargs['service_pk'])
    # def get_serializer_context(self):
    #     return {'service_id': self.kwargs['service_pk']}
    # # def perform_create(self, serializer):
    # #     serializer.save(user=self.request.user)