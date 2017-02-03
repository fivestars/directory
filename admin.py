from django.contrib import admin
from directory.models import Department, Location, Employee, Pet


class DepartmentAdmin(admin.ModelAdmin):
    # search input looks through name
    search_fields = ["name"]


class LocationAdmin(admin.ModelAdmin):
    # search input looks through name
    search_fields = ["name"]


class EmployeeAdmin(admin.ModelAdmin):
    # search input looks through first name, last name, email
    search_fields = ["first_name", "last_name", "email"]

    # drill down by start date
    date_hierarchy = "start_date"


class PetAdmin(admin.ModelAdmin):
    # search input looks through name
    search_fields = ["name"]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Pet, PetAdmin)
