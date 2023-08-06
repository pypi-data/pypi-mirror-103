from django.urls import include, path
from django.views.generic import TemplateView

from .views import send_push

urlpatterns = [
    path("send_push", send_push),
    path("webpush/", include("webpush.urls")),
]
