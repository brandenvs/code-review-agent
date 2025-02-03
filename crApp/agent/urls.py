from django.urls import path
from agent import views

urlpatterns = [
    path('', views.index, name="home"),
]
