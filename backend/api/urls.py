from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.EntryListCreate.as_view(), name="entries-list"),
    path("entries/delete/<int:pk>/", views.EntryDelete.as_view(), name="delete-entry"),
    path("entries/update/<int:pk>/", views.EntryUpdate.as_view(), name="update-entry"),
    path("accounts/", views.AccountListCreate.as_view(), name="account-list"),
    path("accounts/delete/<int:pk>/", views.AccountDelete.as_view(), name="delete-account"),
    path("categories/", views.CategoryListCreate.as_view(), name="category-list-create"),
]