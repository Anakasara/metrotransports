from django.urls import path
from .views import (
    CustomerListCreateView,
    EmployeeListCreateView,
    TractorListCreateView,
    EmployeeListView,
    AttendanceSubmissionView,
    TractorListView,
    TractorHoursSubmissionView,
    JobSubmissionView,
    CustomerListView,
    ReceiptCreateView,
    AttendanceReportView,
    SalesReportView,
    TractorHoursReportView,
    CustomerLedgerView,
    TotalCustomerOutstandingView,
    api_overview  # Import the new view here
)

urlpatterns = [
    path('', api_overview, name='api-overview'),  # Add this line for the base api endpoint
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/list/', CustomerListView.as_view(), name='customer-list'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/list/', EmployeeListView.as_view(), name='employee-list'),
    path('tractors/', TractorListCreateView.as_view(), name='tractor-list-create'),
    path('tractors/list/', TractorListView.as_view(), name='tractor-list'),
    path('attendance/submit/', AttendanceSubmissionView.as_view(), name='attendance-submit'),
    path('tractor-hours/submit/', TractorHoursSubmissionView.as_view(), name='tractor-hours-submit'),
    path('jobs/submit/', JobSubmissionView.as_view(), name='job-submission'),
    path('receipts/', ReceiptCreateView.as_view(), name='receipt-create'),
    path('attendance-report/', AttendanceReportView.as_view(), name='attendance-report'),
    path('sales-report/', SalesReportView.as_view(), name='sales-report'),
    path('tractor-hours-report/', TractorHoursReportView.as_view(), name='tractor-hours-report'),
    path('customer-ledger/', CustomerLedgerView.as_view(), name='customer-ledger'),
    path('total-customer-outstanding/', TotalCustomerOutstandingView.as_view(), name='total-customer-outstanding')
]
