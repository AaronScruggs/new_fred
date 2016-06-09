from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView,\
    RedirectView, UpdateView, DeleteView
from rest_framework.authtoken.models import Token

from advertisements.forms import AdvertisementForm, AdvertisementUpdateForm
from advertisements.models import Advertisement, SubCategory, Category, City

import logging

logger = logging.getLogger("ads")

def get_current_city(request):
    """
    Checks for a city to filter results on. First the user profile is checked
    for a preference, then the session.
    :param request: Any self.request.
    :return: The proper city or None.
    """
    city_id = request.session.get("city_id", None)

    if hasattr(request.user, "profile") and hasattr(
            request.user.profile, "city"):
        return request.user.profile.city
    elif request.session.get("city_id", None):
        return City.objects.get(pk=city_id)
    else:
        return None


def query_sort(get, qs):
    """
    This is a helper function for use inside get_queryset.
    :param get: A self.request.GET object possibly containing a querystring
    parameter for sorting advertisements.
    :param qs: The queryset for a category or subcategory.
    :return: A sorted queryset.
    """

    if "price" in get and get["price"] == "low":
        qs = qs.order_by("price")
    elif "price" in get and get["price"] == "high":
        qs = qs.order_by("-price")
    elif "modified" in get and get["modified"] == "new":
        qs = qs.order_by("-modified_time")
    elif "modified" in get and get["modified"] == "old":
        qs = qs.order_by("modified_time")

    return qs


class MainPageView(ListView):
    template_name = "advertisements/main_page.html"
    context_object_name = "categories"

    def get_queryset(self):
        """
        :return: A queryset of all categories and thier associated
        subcategories.
        """
        qs = []
        for cat in Category.objects.select_related().all():
            qs.append((cat, SubCategory.objects.filter(category=cat)))

        return qs

    def get_context_data(self, **kwargs):
        """
        If the session has a city selected 'city_title' will be created with
        its title.
        'cities' is a list of all cities in the database which are placed
        in the template with redirect links to select or change the city
        for the current session.
        """
        context = super().get_context_data(**kwargs)
        city = get_current_city(self.request)

        if city:
            context["city_title"] = city.title

        context["cities"] = City.objects.all()
        return context


class CategoryView(ListView):

    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"
    paginate_by = 20

    def get_queryset(self):
        """
        :return: A queryset filtered by city and category.
        """
        logger.debug("category test")

        category = Category.objects.get(pk=self.kwargs["pk"])
        city = get_current_city(self.request)
        logger.debug("category city: {}".format(city))

        qs = Advertisement.objects.select_related("city").filter(
            subcategory__category=category)

        if city:
            qs = qs.filter(city__id=city.id)

        return query_sort(self.request.GET, qs)

    def get_context_data(self, **kwargs):
        """
        view is the display view ('list', 'thumb', or 'gallery') selected
        by the user.
        """
        logger.info("category info")
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs["pk"])
        context["category"] = category

        view = self.request.GET.get("view", "list")
        context['view'] = view
        return context


class SubCategoryView(ListView):
    """
    This view is the same as CategoryView outside of the category filtering.
    """
    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"
    paginate_by = 20

    def get_queryset(self):
        logger.debug("test")

        subcategory = SubCategory.objects.get(pk=self.kwargs["pk"])
        logger.debug("subcat: {}".format(subcategory))

        city = get_current_city(self.request)
        logger.debug("city: {}".format(city))

        qs = Advertisement.objects.select_related("city").filter(
            subcategory=subcategory)
        if city:
            qs = qs.filter(city__id=city.id)

        return query_sort(self.request.GET, qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = SubCategory.objects.get(pk=self.kwargs["pk"])
        context["category"] = category

        view = self.request.GET.get("view", "list")
        context['view'] = view
        return context


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = "advertisements/advertisement_detail.html"
    context_object_name = "advertisement"


class AdvertisementCreate(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy("main_page")
    template_name = "advertisements/advertisement_create.html"

    def form_valid(self, form):
        if self.request.user.pk:
            form.instance.user = self.request.user
        form.instance.city = get_current_city(self.request)
        return super().form_valid(form)


class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementUpdateForm
    template_name = "advertisements/advertisement_update.html"
    success_url = reverse_lazy("main_page")


class AdvertisementDelete(DeleteView):
    model = Advertisement
    template_name = "advertisements/advertisement_delete.html"
    success_url = reverse_lazy("main_page")


class AllCityList(ListView):
    model = City
    context_object_name = "cities"
    template_name = "advertisements/all_cities.html"


class CityRedirect(RedirectView):
    pattern_name = "city_redirect"
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        chosen_city = get_object_or_404(City, pk=self.kwargs["id"])
        self.request.session["city_id"] = chosen_city.id
        if self.request.user.pk:
            self.request.user.profile.city = chosen_city
            self.request.user.profile.save()
        return reverse("main_page")


class UserDetail(LoginRequiredMixin, ListView):
    template_name = "advertisements/user_detail.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        """
        :return: All of the users advertisements, sorted by the most recently
        created or modified.
        """

        profiled_user = User.objects.get(pk=self.kwargs['pk'])
        return Advertisement.objects.filter(
            user=profiled_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiled_user = User.objects.get(pk=self.kwargs['pk'])
        context["profiled_user"] = profiled_user
        context["user_match"] = self.request.user == profiled_user

        user_token = Token.objects.filter(user=profiled_user)[0]
        context["token"] = user_token

        new_token = self.request.GET.get("token")
        if new_token == "new":
            user_token.delete()
            context["token"] = Token.objects.create(user=profiled_user)

        return context
