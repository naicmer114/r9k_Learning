from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('post/<int:id_post>', views.post_base)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)