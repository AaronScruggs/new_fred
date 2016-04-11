from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, RedirectView, UpdateView, DeleteView

from advertisements.forms import AdvertisementForm, AdvertisementUpdateForm
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


def query_sort(get, qs):

    if "price" in get and get["price"] == "low":
        qs = qs.order_by("price")
    elif "price" in get and get["price"] == "high":
        qs = qs.order_by("-price")

    if "modified" in get and get["modified"] == "new":
        qs = qs.order_by("-modified_time")
    elif "modified" in get and get["modified"] == "old":
        qs = qs.order_by("modified_time")

    return qs


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

        context["cities"] = City.objects.all()
        return context


class CategoryView(ListView):


    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs["pk"])
        city = get_current_city(self.request)

        qs = Advertisement.objects.filter(subcategory__category=category)

        if city:
            qs = qs.filter(city__id=city.id)

        return query_sort(self.request.GET, qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs["pk"])
        context["category"] = category

        view = self.request.GET.get("view", "list")
        context['view'] = view
        return context


class SubCategoryView(ListView):
    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        subcategory = SubCategory.objects.get(pk=self.kwargs["pk"])
        city = get_current_city(self.request)

        qs = Advertisement.objects.filter(subcategory=subcategory)
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
        if self.request.user.pk:
            form.instance.user = self.request.user
        form.instance.city = get_current_city(self.request)
        return super().form_valid(form)


class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementUpdateForm
    template_name = "advertisements/advertisement_update.html"
    success_url = reverse_lazy("main_page")
    pk_url_kwarg = "id"


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


class UserDetail(ListView):
    template_name = "advertisements/user_detail.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        # pretty this up when i make docs

        profiled_user = User.objects.get(pk=self.kwargs['pk'])
        return Advertisement.objects.filter(
            user=profiled_user).order_by("-modified_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiled_user = User.objects.get(pk=self.kwargs['pk'])
        context["profiled_user"] = profiled_user
        context["user_match"] = self.request.user == profiled_user
        return context
