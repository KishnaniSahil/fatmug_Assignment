from django.contrib import admin

from vendorManagementSystem.models import HistoricalPerformance, Vendor

# Register your models here.
admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)

