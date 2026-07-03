# Jingisukan Izakaya Django Site

Django rebuild of the restaurant website. The public UI keeps the current CSS/classes/assets from the frontend so the landing page, blog pages, booking form, animations, and mobile layout stay visually aligned with the existing design.

## Pages

- `/en/`, `/jp/`, `/ru/`, `/uz/` - localized landing pages
- `/<locale>/blog/` - localized blog listing
- `/<locale>/blog/<slug>/` - localized blog detail
- `/backoffice/login/` - simple restaurant back office login
- `/backoffice/bookings/` - booking dashboard with date filters and status updates
- `/backoffice/posts/` - blog post management
- `/main-admin/` - default Django admin

## Local Run

```bash
cd "/Users/javo/Desktop/Uravo_restorant/jingisukan_django"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open:

```txt
http://127.0.0.1:8000/en/
```

Set your back office password in `.env`:

```txt
change-this-admin-password
```

You can also change the backoffice password later from `/main-admin/` in Restaurant settings.

## cPanel Notes

For Python app hosting, set the startup WSGI file to:

```txt
passenger_wsgi.py
```

Then run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
