from django.contrib import admin
from ad_sales import models

admin.site.register(models.User_info)
admin.site.register(models.Spot)
admin.site.register(models.Order)
admin.site.register(models.Prototype)
admin.site.register(models.Tag)
# Register your models here.
