from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer,Product,Category
from account.forms import ProductForm

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == "POST":
       username=request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(username=username,password=password)
       if user is not None:
           login(request,user)
           return redirect('/')
       messages.info(request,"login failed please try agian");
      
    return render(request, 'accounts/login.html' )
        
def user_register(request):
    if request.method == "POST":
       username = request.POST.get('username')
       email = request.POST.get('email')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm_password')
       phone = request.POST.get('phone_numberfield')
       
       if password==confirm_password:
            if User.objects.filter(username=username).exists():
               print("user exits")
               messages.info(request,"username is exi");  
            else:
                if User.objects.filter(email=email).exists():
                   print("email alredy exists")
                   messages.info(request,"email exitss");  
                else:
                   user= User.objects.create_user(username=username,email=email,password=password,confirm_password=confirm_password)      
                   user.save()
                   data = Customer(user=user,phone_numberfield=phone)
                   data.save()
                   
                   our_user = authenticate(username=username,password=password)
                   if our_user is not None:
                       login(request,user)
                       return redirect('/')
                   messages.info(request,"please try again");
       else:
            messages.info(request,"password mismatch ");
            print("asd")
            return redirect('user_register')                
    return render(request, 'accounts/registera.html', {'data':data} )
def user_logout(request):
    logout(request)
    return redirect('/')    

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            print(form)
            print("wewe")
            form.save()
            print("saved")
            messages.info(request,"product was saved")
            return redirect('add_product')
        else:
            messages.info(request,"product not addes")
    else:
        print("notsaved")
        form=ProductForm()  
        messages.info(request,"add all")
    
    return render(request, 'snr/addproduct.html',context={'form':form})


