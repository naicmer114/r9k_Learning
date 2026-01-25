from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("post/<int:id_post>", views.post_base),
    # Login
    path("registro/", views.registro, name="registro"),
    path("login/", views.login, name="login"),
    path("logout", views.logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
