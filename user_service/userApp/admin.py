from django.contrib import admin
from .models import CustomUser

# Register CustomUser with the admin interface
admin.site.register(CustomUser)
