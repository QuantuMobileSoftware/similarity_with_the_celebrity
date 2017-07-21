"""
Person admin module
"""
from django.contrib import admin
from person.models import Person, Face


class PersonAdmin(admin.ModelAdmin):
    """
    Person admin
    """
    fieldsets = [
        ('General information', {'fields': ['first_name', 'last_name']}),
    ]
    list_display = ('first_name', 'last_name',)
    list_filter = ['first_name', 'last_name']


class FaceAdmin(admin.ModelAdmin):
    """
    Face admin
    """
    fieldsets = [
        ('General information', {'fields': ['person', 'encoding']}),
    ]
    list_display = ('person',)
    list_filter = ['person']


admin.site.register(Person, PersonAdmin)
admin.site.register(Face, FaceAdmin)
