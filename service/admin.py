from django.contrib import admin
from service.models import Service,Category,Review,ServiceImage
# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(Review)
admin.site.register(Category)
