from django.contrib import admin

from .forms import BlogPostForm, RestaurantSettingsForm
from .models import BlogPost, Booking, RestaurantSettings


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ("title_en", "slug", "date", "status", "updated_at")
    list_filter = ("status", "date")
    search_fields = ("title_en", "title_jp", "title_ru", "title_uz", "slug")
    prepopulated_fields = {"slug": ("title_en",)}
    fieldsets = (
        ("Common settings", {"fields": ("slug", "date", "status", "image", "image_file")}),
        ("English", {"fields": ("title_en", "summary_en", "content_en")}),
        ("Japanese", {"fields": ("title_jp", "summary_jp", "content_jp")}),
        ("Russian", {"fields": ("title_ru", "summary_ru", "content_ru")}),
        ("Uzbek", {"fields": ("title_uz", "summary_uz", "content_uz")}),
    )

    class Media:
        css = {"all": ("css/admin_blog.css",)}
        js = ("js/backoffice.js",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone", "booking_date", "booking_time", "people_count", "locale", "status")
    list_filter = ("status", "locale", "booking_date")
    search_fields = ("customer_name", "phone")


@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    form = RestaurantSettingsForm
    list_display = ("__str__", "updated_at")
    fieldsets = (
        ("Logo", {"fields": ("logo", "logo_path")}),
        ("Backoffice access", {"fields": ("backoffice_password",)}),
        ("Map", {"fields": ("map_iframe_src",)}),
    )

    def has_add_permission(self, request):
        return not RestaurantSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
