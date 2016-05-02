from django.conf.urls import url

from advertisements.views import AdvertisementDetail, AdvertisementCreate, \
    AdvertisementUpdate, AdvertisementDelete

urlpatterns = [url(r'^(?P<pk>\d+)/$', AdvertisementDetail.as_view(),
                   name="advertisement_detail"),
               url(r'^create/$', AdvertisementCreate.as_view(),
                    name="advertisement_create"),
               url(r'^update/(?P<pk>\d+)/$', AdvertisementUpdate.as_view(),
                    name="advertisement_update"),
               url(r'^delete/(?P<pk>\d+)/$', AdvertisementDelete.as_view(),
                   name="advertisement_delete"),
               ]
