from django.contrib import admin
from .models import Item, Manufacture, Upcoming_Product, Contact


admin.site.site_header = "RETECH Mall"
admin.site.site_title = "RETECH Mall"

# Register your models here.
admin.site.register(Item)
admin.site.register(Manufacture)
admin.site.register(Upcoming_Product)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','subject']
    
admin.site.register(Contact, ContactAdmin)
