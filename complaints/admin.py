from django.contrib import admin
from .models import ComplainOutcome , Complain
from complaints.models import Complain, Service
# Register your models here.

admin.site.register(ComplainOutcome)
admin.site.register(Complain)
admin.site.register(Service)


