from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/bookings/", views.booking_create, name="booking_api"),
    path("backoffice/", views.backoffice_home, name="backoffice_home"),
    path("backoffice/login/", views.backoffice_login, name="backoffice_login"),
    path("backoffice/logout/", views.backoffice_logout, name="backoffice_logout"),
    path("backoffice/bookings/", views.backoffice_bookings, name="backoffice_bookings"),
    path("backoffice/bookings/<uuid:pk>/status/", views.backoffice_booking_status, name="backoffice_booking_status"),
    path("backoffice/bookings/<uuid:pk>/delete/", views.backoffice_booking_delete, name="backoffice_booking_delete"),
    path("backoffice/posts/", views.backoffice_posts, name="backoffice_posts"),
    path("backoffice/posts/new/", views.backoffice_post_form, name="backoffice_post_new"),
    path("backoffice/posts/<uuid:pk>/edit/", views.backoffice_post_form, name="backoffice_post_edit"),
    path("backoffice/posts/<uuid:pk>/delete/", views.backoffice_post_delete, name="backoffice_post_delete"),
    path("<str:locale>/", views.landing, name="landing"),
    path("<str:locale>/bookings/create/", views.booking_create, name="booking_create"),
    path("<str:locale>/blog/", views.blog_list, name="blog_list"),
    path("<str:locale>/blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
]
