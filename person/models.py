"""
Person models module
"""
from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    """
    Person model
    """
    first_name = models.CharField('First name', max_length=55)
    last_name = models.CharField('Last name', max_length=55)

    def __unicode__(self):
        """
        Person name and surname
        :return: person full name
        """
        return '{} {}'.format(self.first_name, self.last_name)


class Face(models.Model):
    """
    Face model
    """
    person = models.ForeignKey(Person, verbose_name='Person')
    encoding = models.TextField('Encoding')
