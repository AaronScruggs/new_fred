from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from faker import Faker
from rest_framework import status
from advertisements.models import City, Advertisement, SubCategory, Category
from advertisements.views import get_current_city, query_sort
from profiles.models import Profile
from django.core.urlresolvers import reverse


class ViewFunctionSessionTests(TestCase):

    def setUp(self):
        fake = Faker()
        self.factory = RequestFactory()

        # Made up city for user2.
        self.city_of_oz = City.objects.create(title="OZ")
        self.category = Category.objects.create(title="testcat")
        self.subcategory = SubCategory.objects.create(title="test",
                                                      category=self.category)

        self.user1 = User.objects.create_user(username=fake.name(),
                                              email=fake.email(),
                                              password="blahblah")
        self.user2 = User.objects.create_user(username=fake.name(),
                                              email=fake.email(),
                                              password="blahblah")

        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2,
                                               city=self.city_of_oz)
        # create 3 advertisements with price of 1,2,3.
        self.advertisement1 = [Advertisement.objects.create(
            title=fake.bs(), description=fake.bs(), email=fake.email(),
            city=self.city_of_oz, subcategory=self.subcategory, price=x)
                               for x in range(3)
                               ]

    """
    Test that get_current_city is recognizing the users current active city.
    """

    def test_get_current_city_none(self):
        request = self.factory.get("/mainpage")
        request.session = {}
        request.user = self.user1
        self.assertEqual(get_current_city(request), None)

    def test_get_current_city_true(self):
        request = self.factory.get("/mainpage")
        request.session = {}
        request.user = self.user2
        self.assertEqual(get_current_city(request), self.city_of_oz)

    """
    Test that the query_sort function is correctly sorting querysets according
    to a request querystring. Also test that context_data contains the
    right values.
    """

    def test_query_sort_high(self):
        request = self.factory.get("/subcategory/{}/?price=high".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertGreater(sorted_qs.first().price, sorted_qs.all()[1].price)
        self.assertEqual(request.GET["price"], "high")

    def test_query_sort_low(self):
        request = self.factory.get("/subcategory/{}/?price=low".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertLess(sorted_qs.first().price, sorted_qs.all()[1].price)
        self.assertEqual(request.GET["price"], "low")

    def test_query_sort_blank(self):
        request = self.factory.get("/subcategory/{}".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertGreater(sorted_qs.first().price, sorted_qs.all()[1].price)
        self.assertEqual(request.GET.get("price", None), None)


class CategoryTests(TestCase):
    """
    Test that category and subcategory requests are returning the correct
    advertisements.
    """

    def setUp(self):
        fake = Faker()
        self.city = City.objects.create(title="test city")
        self.category = Category.objects.create(title="test cat")
        self.subcategory1 = SubCategory.objects.create(title="test subcat",
                                                       category=self.category
                                                       )
        self.subcategory2 = SubCategory.objects.create(title="test subcat2",
                                                       category=self.category
                                                       )
        self.advertisements1 = [Advertisement.objects.create(
            title=fake.bs(), description=fake.bs(), email=fake.email(),
            city=self.city, subcategory=self.subcategory1, price=x)
                               for x in range(3)
                               ]
        self.advertisements2 = [Advertisement.objects.create(
            title=fake.bs(), description=fake.bs(), email=fake.email(),
            city=self.city, subcategory=self.subcategory2, price=x)
                                for x in range(2)
                                ]

    def test_category_queryset(self):
        self.url = "/category/{}/".format(self.category.id)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context_data["advertisements"].count(), 5)

    def test_subcategory1_queryset(self):
        self.url = "/subcategory/{}/".format(self.subcategory1.id)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context_data["advertisements"].count(), 3)

    def test_subcategory2_queryset(self):
        self.url = "/subcategory/{}/".format(self.subcategory2.id)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context_data["advertisements"].count(), 2)














