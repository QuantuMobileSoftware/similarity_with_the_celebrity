"""
Person admin module
"""
from django.contrib import admin
from person.models import Person


class PersonAdmin(admin.ModelAdmin):
    """
    Person admin
    """
    fieldsets = [
        ('General information', {'fields': ['name', 'image_link', 'face_encoding']}),
    ]
    list_display = ('name', 'image_link',)
    list_filter = ['name']


admin.site.register(Person, PersonAdmin)
