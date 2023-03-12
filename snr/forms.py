from django import forms

from .models import Checkout
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from account.models import Product,Category,Customer



class CheckoutForm(forms.Form):
    
    
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form_control','placeholder':'wqw street adds'}))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form_control','placeholder':'wqw street adds'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget({'class':'class 10px'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form_control','placeholder':'zip'}))
    
    