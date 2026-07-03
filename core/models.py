import os
import re
import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, max_length=180, blank=True)
    image = models.CharField(max_length=255, default="assets/images/restaurant-hero-table.png")
    image_file = models.FileField(upload_to="blog/", blank=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    title_en = models.CharField(max_length=220)
    title_jp = models.CharField(max_length=220, blank=True)
    title_ru = models.CharField(max_length=220, blank=True)
    title_uz = models.CharField(max_length=220, blank=True)
    summary_en = models.TextField()
    summary_jp = models.TextField(blank=True)
    summary_ru = models.TextField(blank=True)
    summary_uz = models.TextField(blank=True)
    content_en = models.TextField()
    content_jp = models.TextField(blank=True)
    content_ru = models.TextField(blank=True)
    content_uz = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en) or uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image_file:
            return self.image_file.url
        if self.image.startswith(("http://", "https://", "/")):
            return self.image
        return f"/static/{self.image}"

    def __str__(self):
        return self.title_en


class Booking(models.Model):
    NEW = "new"
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    STATUS_CHOICES = ((NEW, "New"), (ACCEPTED, "Accepted"), (CANCELED, "Canceled"))
    LOCALE_CHOICES = (("en", "English"), ("jp", "Japanese"), ("ru", "Russian"), ("uz", "Uzbek"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=180)
    phone = models.CharField(max_length=80)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    people_count = models.PositiveIntegerField()
    locale = models.CharField(max_length=2, choices=LOCALE_CHOICES, default="en")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "booking_time", "-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.booking_date} {self.booking_time}"


DEFAULT_MAP_IFRAME_SRC = "https://www.google.com/maps?q=Chingiz%20Aytmatov%2044%2C%20Yunusabad%2C%20Tashkent&output=embed"


class RestaurantSettings(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    logo = models.FileField(upload_to="settings/", blank=True)
    logo_path = models.CharField(
        max_length=255,
        default="assets/images/logo.jpg",
        help_text="Fallback static logo path. Used when no logo file is uploaded.",
    )
    backoffice_password_hash = models.CharField(max_length=255, blank=True, editable=False)
    map_iframe_src = models.TextField(
        blank=True,
        default=DEFAULT_MAP_IFRAME_SRC,
        help_text="Paste a Google Maps iframe src URL or the full iframe code.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant setting"
        verbose_name_plural = "Restaurant settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        if not self.backoffice_password_hash:
            self.backoffice_password_hash = make_password(os.environ.get("ADMIN_PASSWORD", "change-this-admin-password"))
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        if self.logo_path.startswith(("http://", "https://", "/")):
            return self.logo_path
        return f"{settings.STATIC_URL}{self.logo_path}"

    @property
    def map_embed_src(self):
        value = (self.map_iframe_src or "").strip()
        if not value:
            return ""
        match = re.search(r"src=[\'\"]([^\'\"]+)", value)
        return match.group(1) if match else value

    def check_backoffice_password(self, raw_password):
        if self.backoffice_password_hash:
            return check_password(raw_password, self.backoffice_password_hash)
        return raw_password == os.environ.get("ADMIN_PASSWORD", "change-this-admin-password")

    def set_backoffice_password(self, raw_password):
        if raw_password:
            self.backoffice_password_hash = make_password(raw_password)

    def __str__(self):
        return "Restaurant settings"
