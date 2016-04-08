from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement, SubCategory, Category, City


class MainPageView(ListView):
    template_name = "advertisements/main_page.html"
    context_object_name = "categories"

    def get_queryset(self):
        qs = []
        for cat in Category.objects.all():
            qs.append((cat, SubCategory.objects.filter(category=cat)))

        return qs



class CategoryView(ListView):

    # need to add category title on page.

    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs["pk"])
        qs = Advertisement.objects.filter(subcategory__category=category)
        return qs


class SubCategoryView(ListView):
    template_name = "advertisements/subcategory.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        subcategory = SubCategory.objects.get(pk=self.kwargs["pk"])
        return Advertisement.objects.filter(subcategory=subcategory).order_by("-created_time")


class AdvertisementDetail(DetailView):
    # Fill out template
    model = Advertisement
    template_name = "advertisements/advertisement_detail.html"
    context_object_name = "advertisement"


class AdvertisementCreate(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy("main_page")
    template_name = "advertisements/advertisement_create.html"
    pk_url_kwarg = "id"  # superfluous?

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AllCityList(ListView):
    model = City
    context_object_name = "cities"
    template_name = "advertisements/all_cities.html"
