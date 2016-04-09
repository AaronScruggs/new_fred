from django import forms
from advertisements.models import Advertisement


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ("title", "description", "price", "subcategory", "phone_number",
                  "image", "email", "zipcode")
