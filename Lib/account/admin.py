from django.contrib import admin
from account.models import Customer,Category,Product
# Register your models here.
admin.site.register(Customer);
class CustomerAdminModel(admin.ModelAdmin):
    list_display=['user','phone_numberfield']

admin.site.register(Category);    
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=['category_name']
    
admin.site.register(Product);
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name','category','desc','price','product_available_count','img']