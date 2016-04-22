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
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from advertisements.views import CategoryView, SubCategoryView, MainPageView,\
    AllCityList, CityRedirect, UserDetail
from profiles.views import RegisterUser

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/register/$', RegisterUser.as_view(), name="register"),
    url(r'^users/detail/(?P<pk>\d+)/$', UserDetail.as_view(),
        name="user_detail"),
    url(r'^advertisements/', include("advertisements.urls")),
    url(r'^subcategory/(?P<pk>\d+)/$',
        cache_page(60 * 5)(SubCategoryView.as_view()),
        name="subcategory_list"),
    url(r'^category/(?P<pk>\d+)/$', cache_page(60 * 5)(CategoryView.as_view()),
        name="category_list"),
    url(r'^allcities/$', AllCityList.as_view(), name="all_cities"),
    url(r'cities/redirect/(?P<id>\d+)/$', CityRedirect.as_view(),
        name="city_redirect"),
    url(r"^api/", include('api.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', logout, {'next_page': reverse_lazy("main_page")},
        name='logout'),
    url(r'^$', MainPageView.as_view(), name="main_page"),
    url('^', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
