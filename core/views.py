from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.contrib import messages
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.utils.html import escape
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .booking_time import booking_window
from .content import HTML_LANG, LOCALE_FLAGS, LOCALE_LABELS, admin_language_links, get_admin_copy, get_copy, get_locale, language_links, localized
from .forms import BlogPostForm
from .models import BlogPost, Booking, RestaurantSettings


def _locale_or_404(locale: str) -> str:
    clean = get_locale(locale)
    if clean != locale:
        raise Http404
    return clean


def _post_card(post: BlogPost, locale: str) -> dict:
    return {
        "id": post.id,
        "slug": post.slug,
        "url": f"/{locale}/blog/{post.slug}/",
        "image": post.image_url,
        "date": post.date.strftime("%b %-d, %Y") if os.name != "nt" else post.date.strftime("%b %#d, %Y"),
        "title": localized(post, "title", locale),
        "summary": localized(post, "summary", locale),
    }


def _site_settings():
    return RestaurantSettings.load()


def _base_context(locale: str) -> dict:
    copy = get_copy(locale)
    site_settings = _site_settings()
    return {
        "locale": locale,
        "html_lang": HTML_LANG.get(locale, "en"),
        "copy": copy,
        "language_links": language_links(locale),
        "locale_label": LOCALE_LABELS[locale],
        "locale_flag": LOCALE_FLAGS[locale],
        "site_settings": site_settings,
        "site_logo_url": site_settings.logo_url,
        "map_iframe_src": site_settings.map_embed_src,
        "meta_title": copy["meta"]["title"],
        "meta_description": copy["meta"]["description"],
    }


def _content_html(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    html_markers = ("<p", "<h1", "<h2", "<h3", "<ul", "<ol", "<li", "<blockquote", "<strong", "<em", "<a", "<br")
    if any(marker in value.lower() for marker in html_markers):
        return value
    paragraphs = [part.strip() for part in value.split("\n\n") if part.strip()]
    return "".join(f"<p>{escape(part).replace(chr(10), '<br>')}</p>" for part in paragraphs)


def home(request):
    return redirect("landing", locale="en")


def landing(request, locale: str):
    locale = _locale_or_404(locale)
    context = _base_context(locale)
    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED)[:3]
    context.update(
        {
            "marquee_items": context["copy"]["marquee"] * 2,
            "posts": [_post_card(post, locale) for post in posts],
            "booking_window": booking_window(),
            "booking_saved": request.GET.get("booking") == "saved",
        }
    )
    return render(request, "landing.html", context)


def blog_list(request, locale: str):
    locale = _locale_or_404(locale)
    context = _base_context(locale)
    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED)
    context.update(
        {
            "meta_title": f"{context['copy']['blog']['title']} | {context['copy']['header']['brand']}",
            "meta_description": context["copy"]["blog"]["intro"],
            "posts": [_post_card(post, locale) for post in posts],
        }
    )
    return render(request, "blog_list.html", context)


def blog_detail(request, locale: str, slug: str):
    locale = _locale_or_404(locale)
    post = get_object_or_404(BlogPost, slug=slug, status=BlogPost.PUBLISHED)
    context = _base_context(locale)
    context.update(
        {
            "post": _post_card(post, locale),
            "post_content": _content_html(localized(post, "content", locale)),
            "meta_title": f"{localized(post, 'title', locale)} | {context['copy']['header']['brand']}",
            "meta_description": localized(post, "summary", locale),
        }
    )
    return render(request, "blog_detail.html", context)


def _json_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
    return request.POST


@require_POST
def booking_create(request, locale: str | None = None):
    data = _json_payload(request)
    locale = get_locale(locale or data.get("locale", "en"))
    errors = []
    try:
        booking_date = datetime.strptime(str(data.get("booking_date", "")), "%Y-%m-%d").date()
        booking_time = datetime.strptime(str(data.get("booking_time", "")), "%H:%M").time()
        people_count = int(data.get("people_count", 0))
    except (TypeError, ValueError):
        errors.append("Invalid date, time, or guest count.")
        booking_date = None
        booking_time = None
        people_count = 0

    customer_name = str(data.get("customer_name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    if not customer_name or not phone or people_count < 1:
        errors.append("Missing required fields.")

    if errors:
        if request.headers.get("accept", "").startswith("application/json") or request.content_type == "application/json":
            return JsonResponse({"ok": False, "errors": errors}, status=400)
        messages.error(request, get_copy(locale)["booking"]["validation"])
        return redirect(f"/{locale}/#booking")

    Booking.objects.create(
        customer_name=customer_name,
        phone=phone,
        booking_date=booking_date,
        booking_time=booking_time,
        people_count=people_count,
        locale=locale,
    )

    if request.headers.get("accept", "").startswith("application/json") or request.content_type == "application/json":
        return JsonResponse({"ok": True})
    return redirect(f"/{locale}/?booking=saved#booking")


def _is_admin(request):
    return bool(request.session.get("restaurant_admin"))


def _require_admin(request):
    if not _is_admin(request):
        return redirect(f"{reverse('backoffice_login')}?next={request.path}")
    return None


def _admin_locale(request) -> str:
    return get_locale(request.GET.get("lang", "en"))


def _admin_context(request, current_path: str, title: str | None = None) -> dict:
    locale = _admin_locale(request)
    copy = get_admin_copy(locale)
    site_settings = _site_settings()
    return {
        "admin_locale": locale,
        "admin_copy": copy,
        "admin_title": title or copy["bookings"]["title"],
        "admin_locale_label": LOCALE_LABELS[locale],
        "admin_locale_flag": LOCALE_FLAGS[locale],
        "site_logo_url": site_settings.logo_url,
        "admin_language_links": admin_language_links(locale, current_path),
        "admin_current_path": current_path,
        "admin_lang_query": f"?lang={locale}",
    }


def _admin_url(name: str, locale: str) -> str:
    return f"{reverse(name)}?lang={locale}"


def _tashkent_today():
    return datetime.now(ZoneInfo("Asia/Tashkent")).date()


def _localized_post_card(post: BlogPost, locale: str) -> dict:
    copy = get_admin_copy(locale)
    title = localized(post, "title", locale)
    return {
        "id": post.id,
        "slug": post.slug,
        "image_url": post.image_url,
        "date": post.date,
        "status": post.status,
        "status_label": copy["postForm"]["published"] if post.status == BlogPost.PUBLISHED else copy["postForm"]["draft"],
        "title": title,
        "summary": localized(post, "summary", locale),
        "delete_message": copy["posts"]["deleteMessage"].format(title=title),
    }


def backoffice_home(request):
    if not _is_admin(request):
        return redirect("backoffice_login")
    return redirect("backoffice_bookings")


def backoffice_login(request):
    locale = _admin_locale(request)
    copy = get_admin_copy(locale)
    if request.method == "POST":
        site_settings = _site_settings()
        if site_settings.check_backoffice_password(request.POST.get("password", "")):
            request.session["restaurant_admin"] = True
            next_url = request.GET.get("next") or _admin_url("backoffice_bookings", locale)
            return redirect(next_url)
        messages.error(request, copy["login"]["wrong"])
    site_settings = _site_settings()
    return render(request, "backoffice/login.html", {"admin_locale": locale, "admin_copy": copy, "admin_locale_label": LOCALE_LABELS[locale], "admin_locale_flag": LOCALE_FLAGS[locale], "site_logo_url": site_settings.logo_url, "admin_language_links": admin_language_links(locale, reverse("backoffice_login"))})


def backoffice_logout(request):
    locale = _admin_locale(request)
    request.session.pop("restaurant_admin", None)
    return redirect(f"{reverse('backoffice_login')}?lang={locale}")


def backoffice_bookings(request):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = _admin_locale(request)
    copy = get_admin_copy(locale)
    today = _tashkent_today()
    tomorrow = today + timedelta(days=1)
    now_time = datetime.now(ZoneInfo("Asia/Tashkent")).time().replace(second=0, microsecond=0)
    date_from = request.GET.get("from", "")
    date_to = request.GET.get("to", "")
    qs = Booking.objects.filter(Q(booking_date__gt=today) | Q(booking_date=today, booking_time__gte=now_time))
    if date_from:
        qs = qs.filter(booking_date__gte=date_from)
    if date_to:
        qs = qs.filter(booking_date__lte=date_to)
    context = _admin_context(request, reverse("backoffice_bookings"), copy["bookings"]["title"])
    context.update(
        {
            "bookings": qs,
            "date_from": date_from,
            "date_to": date_to,
            "today": today.isoformat(),
            "tomorrow": tomorrow.isoformat(),
            "counts": {
                "total": qs.count(),
                "new": qs.filter(status=Booking.NEW).count(),
                "accepted": qs.filter(status=Booking.ACCEPTED).count(),
            },
            "statuses": [Booking.NEW, Booking.ACCEPTED, Booking.CANCELED],
        }
    )
    return render(request, "backoffice/bookings.html", context)


@require_POST
def backoffice_booking_status(request, pk):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = get_locale(request.POST.get("lang", request.GET.get("lang", "en")))
    booking = get_object_or_404(Booking, pk=pk)
    status = request.POST.get("status")
    if status in {Booking.NEW, Booking.ACCEPTED, Booking.CANCELED}:
        booking.status = status
        booking.save(update_fields=["status"])
    return redirect(_admin_url("backoffice_bookings", locale))


@require_POST
def backoffice_booking_delete(request, pk):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = get_locale(request.POST.get("lang", request.GET.get("lang", "en")))
    get_object_or_404(Booking, pk=pk).delete()
    return redirect(_admin_url("backoffice_bookings", locale))


def backoffice_posts(request):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = _admin_locale(request)
    copy = get_admin_copy(locale)
    context = _admin_context(request, reverse("backoffice_posts"), copy["posts"]["title"])
    context.update({"posts": [_localized_post_card(post, locale) for post in BlogPost.objects.all()]})
    return render(request, "backoffice/posts.html", context)


def backoffice_post_form(request, pk=None):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = _admin_locale(request)
    copy = get_admin_copy(locale)
    post = get_object_or_404(BlogPost, pk=pk) if pk else None
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(_admin_url("backoffice_posts", locale))
    current = reverse("backoffice_post_edit", kwargs={"pk": pk}) if pk else reverse("backoffice_post_new")
    context = _admin_context(request, current, copy["postForm"]["editTitle"] if post else copy["postForm"]["newTitle"])
    context.update({"form": form, "post": post})
    return render(request, "backoffice/post_form.html", context)


@require_POST
def backoffice_post_delete(request, pk):
    guard = _require_admin(request)
    if guard:
        return guard
    locale = get_locale(request.POST.get("lang", request.GET.get("lang", "en")))
    get_object_or_404(BlogPost, pk=pk).delete()
    return redirect(_admin_url("backoffice_posts", locale))


def custom_404(request, exception):
    locale = get_locale(getattr(request, "resolver_match", None).kwargs.get("locale", "en") if getattr(request, "resolver_match", None) else "en")
    context = _base_context(locale)
    context.update({
        "meta_title": "Page not found | Jingisukan Izakaya",
        "meta_description": "The page you are looking for could not be found.",
    })
    return render(request, "404.html", context, status=404)
