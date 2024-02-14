from django.contrib import admin
from .models import Packages,Amenities,Places
# Register your models here.
admin.site.register(Packages)
admin.site.register(Amenities)
admin.site.register(Places)