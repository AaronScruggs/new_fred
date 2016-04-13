from django import forms
from advertisements.models import Advertisement


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ("title", "description", "price", "subcategory",
                   "phone_number", "image", "email", "zipcode")


class AdvertisementUpdateForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ("description", "price", "phone_number", "image", "zipcode")


class SearchForm(forms.Form):
    search_box = forms.CharField(max_length=100)
