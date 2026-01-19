from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('post/<int:id_post>', views.post_base)
]

urlpatterns = [
    path('', views.index),
    path('post/<int:id_post>', views.post_base),
    path('registro/', views.registro, name="registro"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]
