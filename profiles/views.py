from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile


class RegisterUser(CreateView):

    model = User
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response


class UpdateProfile(LoginRequiredMixin, UpdateView):

    pass


