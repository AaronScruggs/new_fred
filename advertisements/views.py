from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, RedirectView

from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement, SubCategory, Category, City


def get_current_city(request):
    # return profile city, session city, or none. Checked in that order.
    city_id = request.session.get("city_id", None)

    if hasattr(request.user, "profile") and hasattr(request.user.profile, "city"):
        return request.user.profile.city
    elif request.session.get("city_id", None):
        return City.objects.get(pk=city_id)
    else:
        return None



class MainPageView(ListView):
    template_name = "advertisements/main_page.html"
    context_object_name = "categories"

    def get_queryset(self):
        qs = []
        for cat in Category.objects.all():
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
        # city_id = self.request.session.get("city_id", None)
        #
        # if hasattr(self.request.user, "profile") and hasattr(self.request.user.profile, "city"):
        #     context["city_title"] = self.request.user.profile.city.title
        # elif city_id:
        #     city = City.objects.get(pk=city_id)
        #     context["city_title"] = city.title

        context["cities"] = City.objects.all()
        return context


class CategoryView(ListView):

    # need to add category title on page.

    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs["pk"])
        city = get_current_city(self.request)
        if city:
            return Advertisement.objects.filter(subcategory__category=category, city__id=city.id)
        else:
            return Advertisement.objects.filter(subcategory__category=category)
        # qs = Advertisement.objects.filter(subcategory__category=category)
        # return qs


class SubCategoryView(ListView):
    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        subcategory = SubCategory.objects.get(pk=self.kwargs["pk"])
        city = get_current_city(self.request)
        if city:
            return Advertisement.objects.filter(subcategory=subcategory, city__id=city.id)
        else:
            return Advertisement.objects.filter(subcategory=subcategory)
        #return Advertisement.objects.filter(subcategory=subcategory)


class AdvertisementDetail(DetailView):
    # Fill out template
    model = Advertisement
    template_name = "advertisements/advertisement_detail.html"
    context_object_name = "advertisement"


class AdvertisementCreate(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy("main_page")
    template_name = "advertisements/advertisement_create.html"
    pk_url_kwarg = "id"  # superfluous?

    def form_valid(self, form):
        if self.request.user is User:
            form.instance.user = self.request.user
        form.instance.city = get_current_city(self.request)
        return super().form_valid(form)


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
