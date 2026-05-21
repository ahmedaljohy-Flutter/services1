from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeliveryListView.as_view(), name='delivery_list'),
    path('add/', views.DeliveryCreateView.as_view(), name='delivery_add'),
    path('<int:pk>/edit/', views.DeliveryUpdateView.as_view(), name='delivery_edit'),
    path('<int:pk>/delete/', views.DeliveryDeleteView.as_view(), name='delivery_delete'),
    path('api/', views.DeliveryListCreateAPI.as_view(), name='delivery_api'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register_account'),
]
