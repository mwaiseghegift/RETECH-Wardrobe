from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from  django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    
    def CategoryItems(self):
        return Item.objects.filter(category=self)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "categories"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='item_category', blank = True, null=True)
    description = models.TextField(null=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=10)
    new_price = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null=True)
    pic = models.ImageField(upload_to='images/items', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(270,270)],
                                   format='JPEG',
                                   options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("retechecommerce:item-detail", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("retechecommerce:add-to-cart", kwargs={"slug": self.slug})
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.item
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"
    
class Upcoming_Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=250)
    description = models.TextField(null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    pic = models.ImageField(upload_to='images/items/upcoming', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.names
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
class Manufacture(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200, default="#")
    logo = models.ImageField(upload_to='images/manufactures', default='images/manafactures/default.png')
    logo_thumbnail = ImageSpecField(source='logo',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    

        
    