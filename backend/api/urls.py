from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.EntryListCreate.as_view(), name="entry-list"),
    path("entries/delete/<int:pk>/", views.EntryDelete.as_view(), name="delete-entry"),
    path("accounts/", views.AccountListCreate.as_view(), name="account-list"),
    path("accounts/delete/<int:pk>/", views.AccountDelete.as_view(), name="delete-account"),
]