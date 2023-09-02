from django.contrib import admin

from yektanet import models

# Register your models here.
class PhoneTabulerModel(admin.TabularInline):
    model = models.Phone

class CarAdminModel(admin.ModelAdmin):
    """Car Admin Model"""
    list_display = ["id", "source", "code"]
    list_filter = ["source"]
    search_fields = ["source", "code"]
    list_display_links = ["id", "source"]
    inlines = [PhoneTabulerModel]
    
class PhoneAdminModel(admin.ModelAdmin):
    """Phone Admin Model"""
    list_display = ["id", "phone", "car"]
    search_fields = ["car__source"]
    list_display_links = ["id", "phone"]

class AuthCodeAdminModel(admin.ModelAdmin):
    """Auth Code Admin Panel"""
    list_display = ["id", "phone"]
    list_display_links = ["id", "phone"]
    search_fields = ["phone"]
    
    
admin.site.register(models.Car, CarAdminModel)
admin.site.register(models.Phone, PhoneAdminModel)
admin.site.register(models.AuthCode, AuthCodeAdminModel)
