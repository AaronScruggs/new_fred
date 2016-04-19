from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from advertisements.models import Category, City, SubCategory, Advertisement
from advertisements.views import get_current_city
from api.permissions import IsOwnerOrReadOnly
from api.serializers import CategorySerializer, CitySerializer, \
    SubCategorySerializer, AdvertisementSerializer, UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubCategoryDetail(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ListCreateAdvertisement(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save(city=get_current_city(self.request))

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if "search" in params:
            qs = qs.filter(Q(title__contains=params["search"]) |
                           Q(description__contains=params["search"])
                           )
        return qs


class DetailUpdateDeleteAdvertisement(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = (IsOwnerOrReadOnly,)
