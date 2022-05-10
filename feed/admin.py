from django.contrib import admin
from .models import Product, Price

# Register your models here.
admin.site.register(Price)

class PriceInLineAdmin(admin.TabularInline):
    model = Price
    extra = 0
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInLineAdmin]


admin.site.register(Product, ProductAdmin)
