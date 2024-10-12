from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange
from datetime import date
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.db import models
from rest_framework import status
from .models import Customer, Employee, Tractor, Attendance, TractorHours, Receipt, Job, TractorHours
from .serializers import CustomerSerializer, EmployeeSerializer, TractorSerializer, AttendanceSubmissionSerializer, AttendanceSerializer, AttendanceRecordSerializer, TractorHoursSubmissionSerializer, TractorSerializer, JobSubmissionSerializer, ReceiptSerializer, AttendanceReportSerializer, TractorHoursReportSerializer
import traceback
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import serializers
from django.shortcuts import render
from django.views import View


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class TractorListCreateView(generics.ListCreateAPIView):
    queryset = Tractor.objects.all()
    serializer_class = TractorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceSubmissionView(generics.CreateAPIView):
    serializer_class = AttendanceSubmissionSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            date = serializer.validated_data['date']
            attendances = serializer.validated_data['attendances']

            for employee_id, attendance_data in attendances.items():
                employee = Employee.objects.get(id=int(employee_id))
                Attendance.objects.update_or_create(
                    employee=employee,
                    date=date,
                    defaults={
                        'present': attendance_data['present'],
                        'description': attendance_data['description']
                    }
                )

            return Response({'message': 'Attendance submitted successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist as e:
            return Response({'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in AttendanceSubmissionView: {str(e)}")
            print(traceback.format_exc())
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TractorListView(generics.ListAPIView):
    queryset = Tractor.objects.all()
    serializer_class = TractorSerializer

class TractorHoursSubmissionView(generics.CreateAPIView):
    serializer_class = TractorHoursSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        date = serializer.validated_data['date']
        hours = serializer.validated_data['hours']

        for tractor_id, hours_data in hours.items():
            tractor = Tractor.objects.get(id=int(tractor_id))
            TractorHours.objects.update_or_create(
                tractor=tractor,
                date=date,
                defaults={
                    'start_hour': hours_data['start'],
                    'end_hour': hours_data['end'],
                    'total_hours': hours_data['total']
                }
            )

        return Response({'message': 'Tractor hours submitted successfully'}, status=status.HTTP_201_CREATED)

class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class JobSubmissionView(generics.CreateAPIView):
    serializer_class = JobSubmissionSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            jobs = serializer.save()
            return Response({'message': f'{len(jobs)} jobs submitted successfully'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in JobSubmissionView: {str(e)}")
            print(traceback.format_exc())
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReceiptCreateView(generics.CreateAPIView):
    serializer_class = ReceiptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AttendanceReportView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response({"error": "Month and year are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)
            _, days_in_month = monthrange(year, month)
        except ValueError as e:
            print(f"ValueError in AttendanceReportView: {str(e)}")
            return Response({"error": f"Invalid month or year: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = date(year, month, 1)
            end_date = date(year, month, days_in_month)

            employees = Employee.objects.all()
            attendances = Attendance.objects.filter(
                Q(date__gte=start_date) & Q(date__lte=end_date)
            ).select_related('employee')

            attendance_data = {}
            for attendance in attendances:
                date_str = attendance.date.strftime('%Y-%m-%d')
                if date_str not in attendance_data:
                    attendance_data[date_str] = {}
                attendance_data[date_str][attendance.employee.id] = 'Present' if attendance.present else 'Absent'

            serializer = AttendanceReportSerializer({
                'attendance': attendance_data,
                'employees': [{'id': emp.id, 'name': emp.name} for emp in employees]
            })

            return Response(serializer.data)
        except Exception as e:
            print(f"Error in AttendanceReportView: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class SalesReportView(APIView):
    def get(self, request):
        try:
            from_date = request.query_params.get('fromDate')
            to_date = request.query_params.get('toDate')

            if not from_date or not to_date:
                return Response({"error": "Both fromDate and toDate are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            except ValueError as e:
                return Response({"error": f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            jobs = Job.objects.filter(date__range=[from_date, to_date]).values('date', 'customer__name').annotate(total_amount=Sum('load_amount')).order_by('date')
            
            sales_data = [
                {
                    'date': job['date'].strftime('%Y-%m-%d'),
                    'customerName': job['customer__name'],
                    'total_amount': float(job['total_amount'])
                }
                for job in jobs
            ]

            return Response(sales_data)
        except Exception as e:
            print(f"Error in SalesReportView: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TractorHoursReportView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response({"error": "Month and year are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month + 1, 1).date() if month < 12 else datetime(year + 1, 1, 1).date()
        except ValueError:
            return Response({"error": "Invalid month or year"}, status=status.HTTP_400_BAD_REQUEST)

        tractors = Tractor.objects.all()
        tractor_hours = TractorHours.objects.filter(
            date__gte=start_date,
            date__lt=end_date
        ).values('date', 'tractor').annotate(total_hours=Sum('total_hours'))

        tractor_hours_data = {}
        for th in tractor_hours:
            date_str = th['date'].strftime('%Y-%m-%d')
            if date_str not in tractor_hours_data:
                tractor_hours_data[date_str] = {}
            tractor_hours_data[date_str][th['tractor']] = th['total_hours']

        serializer = TractorHoursReportSerializer({
            'tractorHours': tractor_hours_data,
            'tractors': tractors
        })

        return Response(serializer.data)

class CustomerLedgerView(APIView):
    def get(self, request):
        try:
            customer_id = request.query_params.get('customerId')
            from_date = request.query_params.get('fromDate')
            to_date = request.query_params.get('toDate')

            if not customer_id or not from_date or not to_date:
                return Response({"error": "customerId, fromDate, and toDate are required"}, status=status.HTTP_400_BAD_REQUEST)

            customer = Customer.objects.get(id=customer_id)

            # Get opening balance (debit)
            opening_balance = customer.opening_balance

            # Get jobs (debits)
            jobs = Job.objects.filter(
                customer=customer,
                date__range=[from_date, to_date]
            ).annotate(
                amount_dr=F('load_amount'),
                amount_cr=Value(0, output_field=models.DecimalField())
            ).values('date', 'description', 'amount_dr', 'amount_cr')

            # Get receipts (credits)
            receipts = Receipt.objects.filter(
                customer=customer,
                date__range=[from_date, to_date]
            ).annotate(
                amount_dr=Value(0, output_field=models.DecimalField()),
                amount_cr=F('amount_received')
            ).values('date', 'description', 'amount_dr', 'amount_cr')

            # Combine and sort ledger entries
            ledger = sorted(
                list(jobs) + list(receipts),
                key=lambda x: x['date']
            )

            return Response({
                'openingBalance': opening_balance,
                'ledger': ledger
            })
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in CustomerLedgerView: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TotalCustomerOutstandingView(APIView):
    def get(self, request):
        as_on_date = request.query_params.get('asOnDate')

        if not as_on_date:
            return Response({"error": "asOnDate is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            as_on_date = datetime.strptime(as_on_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        customers = Customer.objects.all()
        outstanding_data = []

        for customer in customers:
            jobs_total = Job.objects.filter(customer=customer, date__lte=as_on_date).aggregate(total=Sum('load_amount'))['total'] or 0
            receipts_total = Receipt.objects.filter(customer=customer, date__lte=as_on_date).aggregate(total=Sum('amount_received'))['total'] or 0

            outstanding_data.append({
                'customerName': customer.name,
                'totalAmountDr': float(jobs_total) + float(customer.opening_balance),
                'totalAmountCr': float(receipts_total)
            })

        return Response(outstanding_data)

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')  # Create a template 'home.html'
    
def api_overview(request):
    api_urls = {
        'Customers': {
            'Create/List': '/api/customers/',
            'List All': '/api/customers/list/',
        },
        'Employees': {
            'Create/List': '/api/employees/',
            'List All': '/api/employees/list/',
        },
        'Tractors': {
            'Create/List': '/api/tractors/',
            'List All': '/api/tractors/list/',
        },
        'Attendance': {
            'Submit': '/api/attendance/submit/',
            'Report': '/api/attendance-report/',
        },
        'Sales': {
            'Report': '/api/sales-report/',
        },
        'Tractor Hours': {
            'Submit': '/api/tractor-hours/submit/',
            'Report': '/api/tractor-hours-report/',
        },
        'Customer Ledger': '/api/customer-ledger/',
        'Total Customer Outstanding': '/api/total-customer-outstanding/',
    }
    return JsonResponse(api_urls)