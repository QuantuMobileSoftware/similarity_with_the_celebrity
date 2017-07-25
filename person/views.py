"""
Person views module
"""
import base64
import json
import re
import numpy as np

from io import BytesIO
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from face_recognition_part import get_face_encodings
from person.models import Person

class FaceListCreateAPIView(ListCreateAPIView):
    """
    Get all the faces from the database.
    """

    def get_all_face(self):
        """
        Get all the faces from the database.
        :return: List of the form:
        [{'id': id, 'name': name, 'image_link': image link,
        'face_encoding': [face encoding]}, ...]
        """
        queryset = Person.objects.all()

        all_face = list()
        for person in queryset:
            face = dict()
            face['id'] = person.id
            face['name'] = person.name
            face['image_link'] = person.image_link
            face['face_encoding'] = [np.fromstring(person.face_encoding, dtype=float, sep=',')]
            all_face.append(face)
        return all_face
