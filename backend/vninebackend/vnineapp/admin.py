from django.contrib import admin
from .models import Customer, Employee, Tractor, Attendance, TractorHours, Job, EmployeeJob, Receipt

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'opening_balance')
    search_fields = ('name', 'phone_number')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone_number', 'date_of_joining')
    search_fields = ('name', 'phone_number')
    list_filter = ('role',)

@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tractor_number', 'rc_date')
    search_fields = ('name', 'tractor_number')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'present', 'description')
    list_filter = ('date', 'present')
    search_fields = ('employee__name',)

@admin.register(TractorHours)
class TractorHoursAdmin(admin.ModelAdmin):
    list_display = ('tractor', 'date', 'start_hour', 'end_hour', 'total_hours')
    list_filter = ('date', 'tractor')
    search_fields = ('tractor__name',)

class EmployeeJobInline(admin.TabularInline):
    model = EmployeeJob
    extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'tractor', 'total_load', 'load_rate', 'load_amount')
    list_filter = ('date', 'customer', 'tractor')
    search_fields = ('customer__name', 'tractor__name', 'description')
    inlines = [EmployeeJobInline]

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'amount_received', 'payment_method')
    list_filter = ('date', 'payment_method')
    search_fields = ('customer__name', 'description')

