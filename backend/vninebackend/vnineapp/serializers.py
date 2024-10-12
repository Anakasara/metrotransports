from rest_framework import serializers
from .models import Employee, Attendance, Tractor, TractorHours, Job, EmployeeJob, Customer, Receipt

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'phone_number', 'opening_balance']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'phone_number', 'date_of_joining']

class TractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tractor
        fields = ['id', 'name', 'tractor_number', 'rc_date']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'present', 'description']

class AttendanceRecordSerializer(serializers.Serializer):
    present = serializers.BooleanField()
    description = serializers.CharField(allow_blank=True)

class AttendanceSubmissionSerializer(serializers.Serializer):
    date = serializers.DateField()
    attendances = serializers.DictField(
        child=AttendanceRecordSerializer(),
        allow_empty=False
    )

    def validate_attendances(self, value):
        for employee_id, attendance_data in value.items():
            try:
                Employee.objects.get(id=int(employee_id))
            except (ValueError, Employee.DoesNotExist):
                raise serializers.ValidationError(f"Invalid employee id: {employee_id}")
        return value

class TractorHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = TractorHours
        fields = ['id', 'tractor', 'date', 'start_hour', 'end_hour', 'total_hours']

class TractorHoursSubmissionSerializer(serializers.Serializer):
    date = serializers.DateField()
    hours = serializers.DictField(child=serializers.DictField())

    def validate_hours(self, value):
        for tractor_id, hours_data in value.items():
            try:
                Tractor.objects.get(id=int(tractor_id))
            except (ValueError, Tractor.DoesNotExist):
                raise serializers.ValidationError(f"Invalid tractor id: {tractor_id}")
        return value

class EmployeeJobSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()

    class Meta:
        model = EmployeeJob
        fields = ['employee', 'loading_charge']

class JobSerializer(serializers.ModelSerializer):
    customer = serializers.CharField()
    tractor = serializers.CharField()
    employee_jobs = EmployeeJobSerializer(many=True)

    class Meta:
        model = Job
        fields = ['id', 'date', 'customer', 'tractor', 'total_load', 'load_rate', 'load_amount', 'description', 'employee_jobs']

    def create(self, validated_data):
        employee_jobs_data = validated_data.pop('employee_jobs')
        customer_name = validated_data.pop('customer')
        tractor_name = validated_data.pop('tractor')
        
        customer = Customer.objects.get(name=customer_name)
        tractor = Tractor.objects.get(name=tractor_name)
        
        job = Job.objects.create(customer=customer, tractor=tractor, **validated_data)
        
        for employee_job_data in employee_jobs_data:
            employee_name = employee_job_data.pop('employee')
            employee = Employee.objects.get(name=employee_name)
            EmployeeJob.objects.create(job=job, employee=employee, **employee_job_data)
        
        return job

class JobSubmissionSerializer(serializers.Serializer):
    date = serializers.DateField()
    jobs = JobSerializer(many=True)

    def create(self, validated_data):
        date = validated_data['date']
        jobs_data = validated_data['jobs']
        jobs = []
        for job_data in jobs_data:
            job_data['date'] = date
            job_serializer = JobSerializer(data=job_data)
            job_serializer.is_valid(raise_exception=True)
            jobs.append(job_serializer.save())
        return jobs

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'date', 'customer', 'amount_received', 'payment_method', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = instance.customer.name
        return representation
    
class AttendanceReportSerializer(serializers.Serializer):
    attendance = serializers.DictField()
    employees = serializers.ListField(child=serializers.DictField())

class TractorHoursReportSerializer(serializers.Serializer):
    tractorHours = serializers.DictField()
    tractors = TractorSerializer(many=True)