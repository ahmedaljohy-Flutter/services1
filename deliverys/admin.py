from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('title', 'delivered_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)