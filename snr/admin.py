from django.contrib import admin
from .models import Order,orderd_item
from .models import Checkout
# Register your models here.
admin.site.register(orderd_item);


admin.site.register(Order);
admin.site.register(Checkout);
#class CheckoutModelAdmin(admin.ModelAdmin):
#    list_display = ['user','street_address','apartment_address','country','zip_code']