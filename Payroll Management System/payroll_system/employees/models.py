from django.db import models

class Employee(models.Model):
    EMPLOYEE_TYPES = (
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    employee_type = models.CharField(
        max_length=20,
        choices=EMPLOYEE_TYPES,
        default='FULL_TIME'
    )

    date_joined = models.DateField()

    # Salary Structure
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name