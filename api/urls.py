from api.views import CityList, CategoryList, SubCategoryList, \
    ListCreateAdvertisement, DetailUpdateDeleteAdvertisement, CityDetail, \
    CategoryDetail, SubCategoryDetail, UserList, UserDetail
from django.conf.urls import url


urlpatterns = [
    url(r'^users/$', UserList.as_view(), name="list_users"),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name="detail_user"),
    url(r'^cities/(?P<pk>\d+)/$', CityDetail.as_view(), name="detail_city"),
    url(r'^cities/$', CityList.as_view(), name="list_cities"),
    url(r'^categories/$', CategoryList.as_view(), name="list_categories"),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(), name="detail_category"),
    url(r'^subcategories/$', SubCategoryList.as_view(),
        name="list_subcategories"),
    url(r'^subcategories/(?P<pk>\d+)/$', SubCategoryDetail.as_view(),
        name="subdetail_category"),
    url(r'^advertisements/$', ListCreateAdvertisement.as_view(),
    name="list_create_advertisement"),
    url(r'^advertisements/(?P<pk>\d+)/$', DetailUpdateDeleteAdvertisement.as_view(), name="detail_update_delete_advertisement")
]
