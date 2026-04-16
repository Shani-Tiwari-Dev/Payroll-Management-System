import calendar
from django.db import models
from employees.models import Employee
from attendance.models import Attendance

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def calculate_salary(self):
        total_salary = self.basic_salary + self.hra + self.bonus

        days_in_month = calendar.monthrange(self.year, self.month)[1]

        absents = Attendance.objects.filter(
            employee=self.employee,
            date__month=self.month,
            date__year=self.year,
            status='ABSENT'
        ).count()

        per_day_salary = total_salary / days_in_month
        deduction_amount = per_day_salary * absents

        self.deductions = deduction_amount
        self.net_salary = total_salary - deduction_amount

    def save(self, *args, **kwargs):
        self.calculate_salary()
        super().save(*args, **kwargs)