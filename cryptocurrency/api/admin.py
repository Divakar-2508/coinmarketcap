from django.contrib import admin
from .models import Job, Task, Output, Contract, OfficialLink, Social

# Register your models here.
admin.site.register([Job, Task, Output, Contract, OfficialLink, Social])
