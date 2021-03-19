from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.urls import reverse

from mainstore.models import Category, Item
# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/profile_pics/%Y/%m/%d')
    image_thumbnail = ImageSpecField(
                            source='profile_picture',
                            processors=[ResizeToFill(300,300)],
                            format='JPEG',
                            options={'quality':80})
    tel_no = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username
    
class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username} - {self.company}"