from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.search, name="search"),
    path('searchByIndex/', views.searchByIndex, name="searchByIndex"),
    path("add/", views.addWiki, name="addwiki"),
    path("random/", views.random, name="random"),
    path("edit/<str:title>", views.editWiki, name="editwiki")
]
