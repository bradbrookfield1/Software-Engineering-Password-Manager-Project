from django.urls import path
from .views import (
    AccountListView,
    AccountDetailView,
    AccountDetailViewShown,
    BackToAccountDetailView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
)

urlpatterns = [
    path('', AccountListView.as_view(), name='account-list'),
    path('<int:pk>/', AccountDetailView.as_view(),
         name='account-detail'),
    path('<int:pk>/shown/', AccountDetailViewShown.as_view(), name='account-shown'),
    path('<int:pk>/back/', BackToAccountDetailView.as_view(),
         name='account-back'),
    path('new/', AccountCreateView.as_view(), name='account-create'),
    path('<int:pk>/update/', AccountUpdateView.as_view(), name='account-update'),
    path('<int:pk>/delete/',
         AccountDeleteView.as_view(), name='confirm-delete'),
]
