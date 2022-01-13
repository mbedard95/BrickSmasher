"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from .views import Home, Account, Manage, RentReturn, Users, Movies, Checkouts

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', Home.as_view()),  
    path('account/', Account.as_view()),
    path('manage/', Manage.as_view()),
    path('rentreturn/', RentReturn.as_view()),
    path('account/users/', Users.as_view()),
    path('rentreturn/users/', Users.as_view()),
    path('rentreturn/movies/', Movies.as_view()),
    path('manage/movies/', Movies.as_view()),
    path('rentreturn/checkouts/', Checkouts.as_view()),
    path('rentreturn/checkouts/', Checkouts.as_view()),
]