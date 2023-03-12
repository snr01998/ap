from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Product,Category,Customer
from django_countries.fields import CountryField


# Create your models here.
class orderd_item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    
    def __str__(self):
        return self.product.name
    def _str_(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):
        return self.quantity*self.product.price
    
    def get_final_price(self):
        return self.get_total_item_price()
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(orderd_item)
    start_date=models.DateTimeField(auto_now=True)
    
    ordered_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_id=models.CharField(max_length=130,unique=True,default=None,blank=True,null=True)
    date_timeofpayment =models.DateTimeField(auto_now_add=True) 
    order_deliverd = models.BooleanField(default=False)
    order_reciverd = models.BooleanField(default=False)
    
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=200,null=True,blank=True)
    
    def save(self,*args,**kwargs):
        if self.order_id is None and self.date_timeofpayment and self.id:
            self.order_id = self.date_timeofpayment.strftime('PAY2ME%Y%m%dODR')+ str(self.id)
            
        return super().save(*args,**kwargs)
    def __str__(self):
        return self.user.username 
    
    def get_total_price(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_final_price()
            return int(total)
    def get_total_count():
        order = order.objects.get(pk=self.pk)
        return order.items.count()
    
class Checkout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=130)
    apartment_address = models.CharField(max_length=120)

    country = CountryField(multiple=False)
    
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username    
           
    
    
    

    class Meta:
        verbose_name = ("Checkoutlist")
        verbose_name_plural = ("checkoutlist")

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
 
    