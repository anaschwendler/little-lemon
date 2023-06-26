from django.urls import path
from . import views

urlpatterns = [
    path("welcome/", views.welcome),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("categories/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("categories/<int:pk>", views.SingleMenuItemView.as_view(), name="categories")
]
