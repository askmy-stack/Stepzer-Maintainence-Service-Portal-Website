from django.contrib import admin
from django.urls import path,include
from home import views




urlpatterns = [
   
    path('', views.D1,name='homepage'),
    path('logout', views.logout_view,name='logout'),
    path('employe', views.employe ,name='employe'),
    path('billing', views.billing ,name='billing'),
    path('bills', views.d_bills ,name='bills'),
    path('offline', views.offline ,name='offline'),
    path('offline/<int:mid_t>', views.offline_2 ,name='confirm'),
    path('offline/confirm/<str:nmon>/<str:oid>', views.offline_checkout ,name='checkout'),
    path('settings', views.settings ,name='settings'),
    path('profile', views.profile ,name='profile'),







    # path('billing/checkout/<int:pk>/<int:p>', views.checkout ,name="checkout"),
    path('billing/payment/<str:oid>', views.payment ,name='payment'),

    path('email/str<order_id>/str<email>/', views.send_email ,name="email"),

    # path('signup', views.signup,  name="signup"),

  


    

]

