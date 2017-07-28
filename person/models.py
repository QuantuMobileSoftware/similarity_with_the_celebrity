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
    url = models.CharField('IMDB link', unique=True, null=True, max_length=255)
    image_link = models.CharField('Image link', max_length=255)
    face_encoding = models.TextField('Face encoding')

    def __unicode__(self):
        """
        Person name
        :return: person name
        """
        return self.name

    def __str__(self):
        return "<name={0};link={1};>".format(self.name,self.url)