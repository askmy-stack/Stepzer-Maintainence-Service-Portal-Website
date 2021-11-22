"""maintenence_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pdf', views.pdf),
    path('email', views.send_email,name="mail"),
    # path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    # path('home/', include(('home.urls', 'home'), namespace='home')),
    # path('', views.email),
    path('home/', include(('home.urls', 'home'),namespace="home")),
    # path('signup/', views.signup, name='signup' ),
    path('signup', views.signup, name='signup' ),
    path('login', views.login ,name="login"),
    path('employe', views.employe ,name="employe"),
    path('about', views.about ,name="about"),
    path('contact', views.contact ,name="contact"),
    path('feature', views.feature ,name="feature"),




    path('', views.landingpg, name='landing' ),







    

]
