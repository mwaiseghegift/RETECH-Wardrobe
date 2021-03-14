from django.contrib import admin
from .models import CategoryImage, NewProductCollection
# Register your models here.


class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ['name','image','image_thumbnail']

admin.site.register(CategoryImage, CategoryImageAdmin)

class NewProductCollectionAdmin(admin.ModelAdmin):
    list_display =['name', 'image', 'image_thumbnail']
admin.site.register(NewProductCollection, NewProductCollectionAdmin)