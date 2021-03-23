from django.contrib import admin

# Register your models here.
from . models import Target, Observation
admin.site.register(Target)
admin.site.register(Observation)
