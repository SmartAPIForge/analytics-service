from django.contrib import admin
from .models import Service, RequestData

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(RequestData)
class RequestDataAdmin(admin.ModelAdmin):
    list_display = ('service', 'timestamp', 'response_time', 'success')
    list_filter = ('service', 'success', 'timestamp')
    search_fields = ('service__name',)
    date_hierarchy = 'timestamp'
    list_per_page = 50