from django.urls import path
from .views import (
    DeliveryListView, DeliveryCreateView, DeliveryUpdateView, DeliveryDeleteView,
    DeliveryListCreateAPI
)

urlpatterns = [
    path('', DeliveryListView.as_view(), name='delivery_list'),
    path('add/', DeliveryCreateView.as_view(), name='delivery_add'),
    path('<int:pk>/edit/', DeliveryUpdateView.as_view(), name='delivery_edit'),
    path('<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery_delete'),
    path('api/', DeliveryListCreateAPI.as_view(), name='delivery_api'),
]