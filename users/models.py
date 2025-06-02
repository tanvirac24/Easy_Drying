from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from service.validators import validate_file_size
# Create your models here.
class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    address=models.TextField(blank=True, null=True)
    phone_number=models.CharField()
    bio=models.TextField(blank=True,null=True)
    prof_image = models.ImageField(upload_to="Profile/prof_images/", validators=[validate_file_size],blank=True,null=True)

    USERNAME_FIELD= 'email' #use email instead of username
    REQUIRED_FIELDS = []

    objects=CustomUserManager()

    def __str__(self):
        return self.email