from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delv_name', 'delivered_by', 'created_at')
    search_fields = ('delv_name', 'description')
    list_filter = ('created_at',)