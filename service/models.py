from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator ,MaxValueValidator
from service.validators import validate_file_size
# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.PositiveIntegerField(default=10)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="services")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="services/", validators=[validate_file_size],blank=True,null=True)
    # file = models.FileField(upload_to="Service/files", validators=FileExtensionValidator(['pdf']))

class Review(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    name = models.CharField(max_length=255)
    comment= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by  {self.user.first_name} on {self.service.name}"

#STEPS TO BUILD AN API
# Model
# Serializer
# Viwset
# router