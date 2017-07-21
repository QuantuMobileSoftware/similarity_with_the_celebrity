"""
Person models module
"""
from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    """
    Person model
    """
    name = models.CharField('Name', max_length=55)

    def __unicode__(self):
        """
        Person name
        :return: person name
        """
        return self.name


class Face(models.Model):
    """
    Face model
    """
    person = models.ForeignKey(Person, verbose_name='Person')
    encoding = models.TextField('Encoding')
