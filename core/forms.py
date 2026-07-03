from django import forms

from .models import BlogPost, Booking, RestaurantSettings


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "slug",
            "date",
            "status",
            "image",
            "image_file",
            "title_en",
            "summary_en",
            "content_en",
            "title_jp",
            "summary_jp",
            "content_jp",
            "title_ru",
            "summary_ru",
            "content_ru",
            "title_uz",
            "summary_uz",
            "content_uz",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "summary_en": forms.Textarea(attrs={"rows": 3}),
            "summary_jp": forms.Textarea(attrs={"rows": 3}),
            "summary_ru": forms.Textarea(attrs={"rows": 3}),
            "summary_uz": forms.Textarea(attrs={"rows": 3}),
            "content_en": forms.Textarea(attrs={"rows": 7, "data-rich-text": "true", "class": "rich-text-source"}),
            "content_jp": forms.Textarea(attrs={"rows": 7, "data-rich-text": "true", "class": "rich-text-source"}),
            "content_ru": forms.Textarea(attrs={"rows": 7, "data-rich-text": "true", "class": "rich-text-source"}),
            "content_uz": forms.Textarea(attrs={"rows": 7, "data-rich-text": "true", "class": "rich-text-source"}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["customer_name", "phone", "booking_date", "booking_time", "people_count", "locale"]


class RestaurantSettingsForm(forms.ModelForm):
    backoffice_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Leave empty to keep the current backoffice password.",
        label="Backoffice password",
    )

    class Meta:
        model = RestaurantSettings
        fields = ["logo", "logo_path", "backoffice_password", "map_iframe_src"]
        widgets = {
            "map_iframe_src": forms.Textarea(attrs={"rows": 4}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get("backoffice_password")
        if password:
            instance.set_backoffice_password(password)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
