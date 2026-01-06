from django.db import models

# Create your models here.
from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Parameter(models.Model):
    PARAM_TYPES = [
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
        ('str', 'String'),
    ]
    
    machine = models.ForeignKey(Machine, related_name='parameters', on_delete=models.CASCADE)
    label = models.CharField(max_length=50)  # e.g., "Temperature"
    value = models.CharField(max_length=100) # Store everything as string, cast later
    data_type = models.CharField(max_length=10, choices=PARAM_TYPES, default='str')
    unit = models.CharField(max_length=20, blank=True, null=True) # e.g., "°C" or "RPM"

    def __str__(self):
        return f"{self.label} for {self.machine.name}"