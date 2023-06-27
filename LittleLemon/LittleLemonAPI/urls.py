from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("welcome/", views.welcome),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("categories/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("categories/<int:pk>", views.SingleMenuItemView.as_view(), name="categories"),
    path("secret", views.secret),
    path("manager_view", views.manager_view),
    path("api-token-auth", obtain_auth_token),
]
