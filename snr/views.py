from django.shortcuts import render,redirect
from account.models import Customer,Product,Category
from snr.models import Order,orderd_item,Checkout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from snr.forms import CheckoutForm
from django .http import JsonResponse
import razorpay
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from xhtml2pdf import pisa  
import os

from django.template.loader import get_template

from django.contrib.staticfiles import finders

# Create your views here.
def index(request):
    product=Product.objects.all()   
    return render(request, 'snr/index.html',{'product':product})

def product_desc(request,pk):
    product = Product.objects.get(pk=pk)
    context={
        'product':product,
    }
    return render(request,  'snr/product_desc.html',context)

def add_to_cart(request,pk):
    
    product = Product.objects.get(pk=pk)
    order_item, created = orderd_item.objects.get_or_create(
    
    product = product,
    user = request.user,
    ordered = False,
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"adde quantity")
            return redirect("product_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"item addes to cart")
            return redirect("product_desc",pk=pk)
    else:
        ordered_date = timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"item added to cart")
        return redirect("product_desc",pk=pk)
    
def cartlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order=Order.objects.get(user=request.user,ordered=False)
        return render(request,'snr/cartlist.html',{'order':order})
    return render(request,'snr/cartlist.html',{'message':"cart is empty"})

def addproductplus(request,id):
    
    user=request.user
    
    product = orderd_item.objects.get(id=id,user=user)
    order_qs =Order.objects.filter(user=request.user,ordered=False)
    order = order_qs[0]
    
    product.quantity+=1
    
    product.save()
    

  
    
    
    print(product)
    print(product.quantity)
    messages.info(request,"it was added to cart")
    return redirect('cartlist')   
    
def deleteproductplus(request,id):
    
        
    product = orderd_item.objects.get(id=id)
    product.quantity=0
    product.delete()
    print(product)
    print(product.quantity)
    
    return redirect('cartlist')   
def minusproductplus(request,id):
    
        
    product = orderd_item.objects.get(id=id)
    product.quantity-=1
    product.save()
    if product.quantity<1:
       product.quantity-=1
       product.delete()
       print(product)
       print(product.quantity)
       return redirect('cartlist')  
    return redirect('cartlist')
                                                                     
def Checkout_page(request):
    
    if Checkout.objects.filter(user=request.user).exists(): 
        return render(request,"snr/checkout.html", {"payment_allow":"allow"})                                                                     
    
    if request.method == "POST":
       print("saving mave start")
       form = CheckoutForm(request.POST)
       
       
          
       if form.is_valid():
           street_address = form.cleaned_data.get("street_address")
           apartment_address = form.cleaned_data.get("apartment_address")
           country = form.cleaned_data.get("country")
           zip_code = form.cleaned_data.get("zip_code")
            
           checkout = Checkout(
           user=request.user,
           street_address=street_address,
           apartment_address=apartment_address,
           country=country,
           zip_code=zip_code,)
                
            
                
           checkout.save()
                
           print("it shlwill render summery paage")
          # return render(request, "snr/checkout.html",{"payment_allow":"allow"})
           messages.warning(request,"checkout failed")
           return redirect("Checkout_page")
    else:
        form=CheckoutForm()
        return render(request,"snr/checkout.html",{'form':form})
 
client = razorpay.Client(auth=("rzp_test_esVkEJVwVUzE2T","gbPRyWUp1FoXl7XkLTtcH6se"))
razorpay_id="rzp_test_esVkEJVwVUzE2T";
client.set_app_details({"title" : "<Django>", "version" : "<4.1.6>"})    
def paymentsess(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        print(order)
        address = Checkout.objects.get(user=request.user)
        order_amount=order.get_total_price()
        order_currency = "INR"
        order_recipt = order.order_id
        notes= {
            "street_address":address.street_address,
            "apartment_address":address.apartment_address,
            "country":address.country.name,
            "zip":address.zip_code,
        }
        razorpay_order = client.order.create(
            dict(
                amount=order_amount * 100,
                currency=order_currency,
               # recipt=order_recipt,
                notes=notes,
                payment_capture="0"
            )
            )
        order.razorpay_order_id=razorpay_order["id"]
        order.save()
        return render(request, "snr/paymentsummry.html",{
                "order":order,
                "order_id":razorpay_order["id"],
                "orderId":order.order_id,
                "final_price":order_amount,
                "razorpay_merchant_id":razorpay_id,
        },)  
    except Order.DoesNotExist:
        print("order not found")
        return HttpResponse("404 error")
def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path    

            
def render_pdf_view(request):
    order_id =request.session["order_id"]
    order_db = Order.objects.get(razorpay_order_id=order_id)
    check_outaddress = Checkout.objects.get(user=request.user)
    amount = order_db.get_total_price()
    amount = amount*100
    payment_id = order_db.razorpay_payment_id
    payment_status = request.session["payment_status"]
    
    template_path = 'snr/invoice.html'
    context = {'order':order_db,'payment_status':payment_status,'check_outaddress':check_outaddress}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response    



@csrf_exempt    
def handlerequest(request):
    #user=request.user
    
    #product = orderd_item.objects.get(user=user)
    
    #product.quantity=0
    #product.delete()
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id","")
            order_id = request.POST.get("razorpay_order_id","")
            signature=request.POST.get("razorpay_signature","")
            print(payment_id,order_id,signature)
            params_dict={
                "razorpay_payment_id":payment_id,
                "razorpay_order_id":order_id,
                "razorpay_signature":signature,}
            
            try:
                order_db=Order.objects.get(razorpay_order_id=order_id)
                print("order found")
            except:
                print("ordernot found")
                return HttpResponse(" not found")    
            order_db.razorpay_payment_id = payment_id
            print(order_db.razorpay_payment_id)
            order_db.razorpay_signature = signature
            order_db.save()
            result=client.utility.verify_payment_signature(params_dict)
            print(result)
            print("hh")
            if result == True:
                print(result)
                amount=order_db.get_total_price()
                amount=amount * 100
                payment_status = client.payment.capture(payment_id,amount)
                print("hha")
                print(payment_status)
                if payment_status is not None:
                    check_outaddress = Checkout.objects.get(user=request.user)
                    print(payment_status)
                    
                    order_db.ordered = True
                    print("Asdasdas")
                    order_db.save()
                    print(order_db)
                    print("Asdasdas")    
                    request.session[
                        "order complete"
                    ]="your order is placed"
                    request.session["payment_status"]=payment_status
                    request.session['order_id']=order_id
                   # return render(request,"snr/invoice.html",{'order_id':order_id,'payment_status':payment_status,'check_outaddress':check_outaddress})    
                    return redirect('render_pdf_view')
                else:
                    result = False
                    print("payment failed")
                    
                    order_db.ordered=False
                    order_db.save()
                    request.session[
                        "order failed"
                    ]="order not place"
                    return redirect("/")
            else :
                order_db.ordered=False
                order_db.save()
                return render(request,"snr/paymentfailed.html")
        except:
            return HttpResponse("error occured")              
        
def invoice(request):
    return render(request, "snr/invoice.html") 


