from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    ROLE_CHOICES = [
        ('Driver', 'Driver'),
        ('Loadman', 'Loadman'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.role}"
    
class Tractor(models.Model):
    name = models.CharField(max_length=100)
    tractor_number = models.CharField(max_length=20, unique=True)
    rc_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.tractor_number}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {'Present' if self.present else 'Absent'}"
        
class TractorHours(models.Model):
    tractor = models.ForeignKey(Tractor, on_delete=models.CASCADE, related_name='hours')
    date = models.DateField()
    start_hour = models.FloatField()
    end_hour = models.FloatField()
    total_hours = models.FloatField()

    class Meta:
        unique_together = ('tractor', 'date')

    def __str__(self):
        return f"{self.tractor.name} - {self.date} - {self.total_hours} hours"

class Job(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tractor = models.ForeignKey(Tractor, on_delete=models.CASCADE)
    total_load = models.FloatField()
    load_rate = models.FloatField()
    load_amount = models.FloatField()
    description = models.TextField(blank=True)

class EmployeeJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='employee_jobs')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loading_charge = models.FloatField()

class Receipt(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Gpay', 'Gpay'),
        ('Discount', 'Discount'),
    ]

    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.date} - {self.amount_received}"

