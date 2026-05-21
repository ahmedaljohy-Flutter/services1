from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Delivery
from .forms import DeliveryForm

# REST Framework imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import DeliverySerializer

# ==== ميكسن مخصص لإدارة وتدقيق الصلاحيات بشكل مرن ورسائل عربية أنيقة ====
class DeliveryPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "عذراً، ليس لديك الصلاحية الكافية لإجراء هذه العملية.")
            return redirect('delivery_list')
        return super().handle_no_permission()

# ==== متحكمات نظام الحسابات والتسجيل ====

class CustomLoginView(LoginView):
    template_name = 'deliverys/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "اسم المستخدم أو كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = 'login'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'deliverys/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول باستخدام بياناتك.")
        return super().form_valid(form)

# ==== متحكمات إدارة التوصيل (CRUD Django Views) ====

class DeliveryListView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = 'deliverys/delivery_list.html'
    context_object_name = 'deliveries'

class DeliveryCreateView(DeliveryPermissionRequiredMixin, CreateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'deliverys/delivery_form.html'
    success_url = reverse_lazy('delivery_list')
    permission_required = 'deliverys.add_delivery'

    def form_valid(self, form):
        form.instance.delivered_by = self.request.user
        messages.success(self.request, f"تمت إضافة التوصيلة '{form.instance.delv_name}' بنجاح!")
        return super().form_valid(form)

class DeliveryUpdateView(DeliveryPermissionRequiredMixin, UpdateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'deliverys/delivery_form.html'
    success_url = reverse_lazy('delivery_list')
    permission_required = 'deliverys.change_delivery'

    def form_valid(self, form):
        messages.success(self.request, f"تم تحديث بيانات التوصيلة '{form.instance.delv_name}' بنجاح!")
        return super().form_valid(form)

class DeliveryDeleteView(DeliveryPermissionRequiredMixin, DeleteView):
    model = Delivery
    template_name = 'deliverys/delivery_confirm_delete.html'
    success_url = reverse_lazy('delivery_list')
    permission_required = 'deliverys.delete_delivery'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        delv_name = self.object.delv_name
        self.object.delete()
        messages.success(request, f"تم حذف التوصيلة '{delv_name}' بنجاح.")
        return redirect(success_url)

# ==== REST Framework APIs ====

class DeliveryListCreateAPI(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(delivered_by=self.request.user)