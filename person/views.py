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
from person.models import Person, Face


class FaceListCreateAPIView(ListCreateAPIView):
    """
    Get all the faces from the database.
    """

    def get_all_face(self):
        """
        Get all the faces from the database.
        :return: List of the form:
        [{'id': id, 'first_name': first name, 'last_name': last name,
        'face_encoding': [list of face encoding]}, ...]
        """
        queryset = Face.objects.select_related('person').all()

        all_face = list()
        existing_person_id = []

        for col in queryset:
            if col.person.id in existing_person_id:
                for face in all_face:
                    if face['id'] == col.person.id:
                        face['encodings'].append(np.fromstring(col.encoding, dtype=float, sep=','))
            else:
                face = dict()
                face['id'] = col.person.id
                face['name'] = col.person.name
                face['encodings'] = [np.fromstring(col.encoding, dtype=float, sep=',')]
                existing_person_id.append(col.person.id)
                all_face.append(face)
        return all_face
