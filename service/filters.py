from django_filters.rest_framework import FilterSet
from service.models import Service

class ServiceFilter(FilterSet):
    class Meta:
        model= Service
        fields = {
            'category_id':['exact'],
            'price_per_piece':['gt','lt'],
            
            
        }