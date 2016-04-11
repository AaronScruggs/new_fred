from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from faker import Faker

from advertisements.models import City, Advertisement, SubCategory, Category
from advertisements.views import get_current_city, query_sort
from profiles.models import Profile


class ViewFunctionTests(TestCase):

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
    Test that query_sort is correctly sorting querysets according to a
    request querystring.
    """

    def test_query_sort_high(self):
        request = self.factory.get("/subcategory/{}/?price=high".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertGreater(sorted_qs.first().price, sorted_qs.all()[1].price)

    def test_query_sort_low(self):
        request = self.factory.get("/subcategory/{}/?price=low".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertLess(sorted_qs.first().price, sorted_qs.all()[1].price)

    def test_query_sort_blank(self):
        request = self.factory.get("/subcategory/{}".format(
            self.subcategory.pk))
        qs = Advertisement.objects.filter(subcategory=self.subcategory)
        sorted_qs = query_sort(request.GET, qs)
        self.assertLess(sorted_qs.first().price, sorted_qs.all()[1].price)



