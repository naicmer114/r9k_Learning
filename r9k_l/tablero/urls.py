from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('post/<int:id_post>', views.post_base)
]