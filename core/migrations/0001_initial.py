import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("slug", models.SlugField(blank=True, max_length=180, unique=True)),
                ("image", models.CharField(default="assets/images/restaurant-hero-table.png", max_length=255)),
                ("image_file", models.FileField(blank=True, upload_to="blog/")),
                ("date", models.DateField()),
                ("status", models.CharField(choices=[("draft", "Draft"), ("published", "Published")], default="draft", max_length=20)),
                ("title_en", models.CharField(max_length=220)),
                ("title_jp", models.CharField(blank=True, max_length=220)),
                ("title_ru", models.CharField(blank=True, max_length=220)),
                ("title_uz", models.CharField(blank=True, max_length=220)),
                ("summary_en", models.TextField()),
                ("summary_jp", models.TextField(blank=True)),
                ("summary_ru", models.TextField(blank=True)),
                ("summary_uz", models.TextField(blank=True)),
                ("content_en", models.TextField()),
                ("content_jp", models.TextField(blank=True)),
                ("content_ru", models.TextField(blank=True)),
                ("content_uz", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-date", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("customer_name", models.CharField(max_length=180)),
                ("phone", models.CharField(max_length=80)),
                ("booking_date", models.DateField()),
                ("booking_time", models.TimeField()),
                ("people_count", models.PositiveIntegerField()),
                ("locale", models.CharField(choices=[("en", "English"), ("jp", "Japanese"), ("ru", "Russian"), ("uz", "Uzbek")], default="en", max_length=2)),
                ("status", models.CharField(choices=[("new", "New"), ("accepted", "Accepted"), ("canceled", "Canceled")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["booking_date", "booking_time", "-created_at"]},
        ),
    ]
