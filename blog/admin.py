from django.contrib import admin
from .models import Blog, BlogCategory
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','category','author']
    
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory)