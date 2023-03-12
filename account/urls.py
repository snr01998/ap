from django.urls import path
from account import views

app_name:'account'
urlpatterns = [
    path('user_login',views.user_login,name="user_login"),
    path('user_register',views.user_register,name="user_register"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('add_product/',views.add_product,name="add_product"),
    
    
    
]