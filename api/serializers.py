from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import City, Category, SubCategory, Advertisement


class UserSerializer(serializers.ModelSerializer):
    advertisements = serializers.PrimaryKeyRelatedField(many=True,
                                                        read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'advertisement_set')


class CitySerializer(serializers.ModelSerializer):

    advertisements = serializers.PrimaryKeyRelatedField(many=True,
                                                        read_only=True)

    class Meta:
        model = City
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    subcategory_set = serializers.PrimaryKeyRelatedField(many=True,
                                                         read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    advertisements = serializers.PrimaryKeyRelatedField(many=True,
                                                        read_only=True)

    class Meta:
        model = SubCategory
        fields = "__all__"


class AdvertisementSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = "__all__"
