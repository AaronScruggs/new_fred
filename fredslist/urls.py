"""fredslist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from advertisements.views import CategoryView, AdvertisementDetail, \
    SubCategoryView, AdvertisementCreate, MainPageView, AllCityList
from profiles.views import RegisterUser

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/register/$', RegisterUser.as_view(), name="register"),
    url(r'^advertisements/(?P<pk>\d+)/$', AdvertisementDetail.as_view(), name="advertisement_detail"),
    url(r'^subcategory/(?P<pk>\d+)/$', SubCategoryView.as_view(), name="subcategory_list"),
    url(r'^category/(?P<pk>\d+)/$', CategoryView.as_view(),
        name="category_list"),
    url(r'^advertisements/create/$', AdvertisementCreate.as_view(), name = "advertisement_create"),
    url(r'^mainpage/$', MainPageView.as_view(), name="main_page"),
    url(r'^allcities/$', AllCityList.as_view(), name="all_cities"),
    url('^', include('django.contrib.auth.urls')),
]
