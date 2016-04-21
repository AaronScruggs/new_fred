from django.contrib import admin
from advertisements.models import Advertisement, Category, SubCategory, City


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "subcategory",
                    "user", "archived", "city")
    actions = ["archive_ads"]
    search_fields = ["title", "description"]
    date_hierarchy = "created_time"
    list_filter = ["city", "subcategory"]

    def archive_ads(self, request, queryset):
        queryset.update(archived=True)
    archive_ads.short_description = "Archive Ads"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category")

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("title", "state")

    list_filter = ["state"]