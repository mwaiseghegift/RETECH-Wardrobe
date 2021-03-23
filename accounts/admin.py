from django.contrib import admin
from .models import Profile, Seller, Staff
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Profile, ProfileAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display = ['company','user']
admin.site.register(Seller, SellerAdmin)

class StaffAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(Staff, StaffAdmin)