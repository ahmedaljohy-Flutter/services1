from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Delivery
from .forms import DeliveryForm

# REST Framework imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import DeliverySerializer

# حماية الدوال للمستخدمين المسجلين فقط
decorators = [method_decorator(login_required, name='dispatch')]

# ==== CRUD Django Views ====

@method_decorator(login_required, name='dispatch')
class DeliveryListView(ListView):
    model = Delivery
    template_name = 'deliverys/delivery_list.html'
    context_object_name = 'deliveries'

@method_decorator(login_required, name='dispatch')
class DeliveryCreateView(CreateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'deliverys/delivery_form.html'
    success_url = reverse_lazy('delivery_list')

    def form_valid(self, form):
        form.instance.delivered_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeliveryUpdateView(UpdateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'deliverys/delivery_form.html'
    success_url = reverse_lazy('delivery_list')

@method_decorator(login_required, name='dispatch')
class DeliveryDeleteView(DeleteView):
    model = Delivery
    template_name = 'deliverys/delivery_confirm_delete.html'
    success_url = reverse_lazy('delivery_list')


# ==== API View using DRF ====

class DeliveryListCreateAPI(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(delivered_by=self.request.user)