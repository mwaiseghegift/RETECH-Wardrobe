from django.db import models
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

class CategoryImage(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/utilities/category')
    image_thumbnail = ImageSpecField(source='image',
                                processors = [ResizeToFill(1170,300)],
                                format='JPEG',
                                options = {'quality':100})
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Category Image"
        verbose_name_plural = "Category Images"
        
    def __str__(self):
        return f"{self.name} - {self.image_thumbnail.url}"
    
class NewProductCollection(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/utilities/NewProductCollection')
    image_thumbnail = ImageSpecField(source='image',
                                processors = [ResizeToFill(1920,800)],
                                format='JPEG',
                                options = {'quality':100})
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "New Product Image"
        verbose_name_plural = "New Product Images"
        
    def __str__(self):
        return f"{self.name} - {self.image_thumbnail.url}"