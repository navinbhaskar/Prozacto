from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Assistant)
admin.site.register(Appointment)
admin.site.register(Clinic)
admin.site.register(Medical_Records)
