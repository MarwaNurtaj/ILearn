from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(TypeCast)
admin.site.register(Order)
from .models import Room, Massage

# Register your models here.
admin.site.register(Room)
admin.site.register(Massage)