from django.contrib import admin
from .models import City,Temperature

# Register your models here.
admin.site.register([Temperature,City])