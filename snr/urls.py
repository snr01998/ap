from django.urls import path
from snr import views

app_name:'snr'
urlpatterns = [
    path('',views.index,name='index'),
    path('product_desc/<pk>/',views.product_desc,name='product_desc'),
    path('add_to_cart/<pk>',views.add_to_cart,name='add_to_cart'),
    path('cartlist/',views.cartlist,name='cartlist'),
    path('addproductplus/<int:id>',views.addproductplus,name='addproductplus'),
    path('deleteproductplus/<int:id>',views.deleteproductplus,name='deleteproductplus'),
    path('minusproductplus/<int:id>',views.minusproductplus,name='minusproductplus'),
    path('Checkout_page/',views.Checkout_page,name="Checkout_page"),
    path('paymentsess',views.paymentsess,name="paymentsess"),
    path('handlerequest',views.handlerequest,name="handlerequest"),
    path('invoice',views.invoice,name="invoice"),
    path('render_pdf_view',views.render_pdf_view,name="render_pdf_view")
    
]
