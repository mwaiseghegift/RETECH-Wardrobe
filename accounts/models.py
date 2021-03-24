from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.urls import reverse
from django.utils.text import slugify

from mainstore.models import Category, Item
# Create your models here.
User = get_user_model()

STAFF_CATEGORIES = [
    ('CEO','CEO'),
    ('Manager','Manager'),
    ('Customer Manager','Customer Manager'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/profile_pics/%Y/%m/%d')
    image_thumbnail = ImageSpecField(
                            source='profile_picture',
                            processors=[ResizeToFill(300,300)],
                            format='JPEG',
                            options={'quality':80})
    bio = models.TextField()
    tel_no = models.CharField(max_length=10)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)
    
    
class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username} - {self.company}"
    
    def get_absolute_url(self):
        return self.user.profile.get_absolute_url()
    
    
class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=STAFF_CATEGORIES, max_length=255)
    image = models.ImageField(upload_to='images/staff/%Y/%m/%d')
    image_thumbnail = ImageSpecField(
                            source='image',
                            processors=[ResizeToFill(390,450)],
                            format='JPEG',
                            options={'quality':80})
    twitter = models.URLField()
    instagram = models.URLField()
    facebook = models.URLField()
    google_plus = models.URLField()
    
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return self.user.profile.get_absolute_url()
    