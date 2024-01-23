from django.contrib import admin
from .models import CustomUser, Subdivision, EmployeeKind, SheetItem, OutgoKind, OutgoData, Outgo

admin.site.register(CustomUser)
admin.site.register(Subdivision)
admin.site.register(EmployeeKind)
admin.site.register(SheetItem)
admin.site.register(OutgoKind)
admin.site.register(OutgoData)
admin.site.register(Outgo)
