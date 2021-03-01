from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
ITEM_CATEGORY = [
    ('Fashion','Fashion'),
    ('Watches','Watches'),
    ('Jewelry','Jewelry'),
    ('Engagement & Wedding','Engagement & Wedding'),
    ('Electronics','Electronics'),
    ('Phones & Accessories','Phones & Accessories'),
]

class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(choices=ITEM_CATEGORY, max_length=250)
    description = models.TextField(null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    pic = models.ImageField(upload_to='images/items', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(276,357)],
                                   format='JPEG',
                                   options = {'quality':100})
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Upcoming_Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(choices=ITEM_CATEGORY, max_length=250)
    description = models.TextField(null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    pic = models.ImageField(upload_to='images/items/upcoming', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Manufacture(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200, default="#")
    logo = models.ImageField(upload_to='images/manufactures', default='images/manafactures/default.png')
    logo_thumbnail = ImageSpecField(source='logo',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    
    def __str__(self):
        return self.name
    
     