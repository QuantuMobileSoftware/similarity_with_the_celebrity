"""
Face recognition system views module
"""
import base64
import json
import re
import math
import numpy as np

from io import BytesIO
from PIL import Image
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from face_recognition_part import get_face_encodings, compare_faces
from person.views import FaceListCreateAPIView


class IndexView(TemplateView):
    """
    Main page
    """
    template_name = 'index.html'


class UploadPhoto(APIView):
    """
    Upload photo.
    """
    def post(self, request, *args, **kwargs):
        """
        Upload photo.
        :param request:
        :param args:
        :param kwargs:
        :return: information about photo.
        """
        request_data = request.data.get("data")
        image_data = re.sub('data:image/\w*;base64,', '', request_data)
        image = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
        numpy_image = np.array(image)

        unknown_faces_encoding = get_face_encodings(numpy_image)
        data = dict()
        if len(unknown_faces_encoding) != 1:
            data['status'] = 'BAD_REQUEST'
            data['message'] = 'Please make photo with only your face!'
            return Response(json.dumps(data), status=status.HTTP_200_OK)
        face = FaceListCreateAPIView()
        faces = face.get_all_face()
        if len(faces) == 0:
            data['status'] = 'UNKNOWN'
            data['message'] = 'You are unique and unrepeatable. You do not look like any of the celebrities!'
            return Response(json.dumps(data), status=status.HTTP_200_OK)
        result = compare_faces(faces, unknown_faces_encoding[0])
        if not result:
            data['status'] = 'UNKNOWN'
            data['message'] = 'You are unique and unrepeatable. You do not look like any of the celebrities!'
            return Response(json.dumps(data), status=status.HTTP_200_OK)
        data['status'] = 'OK'
        persons = []
        sum_of_all_keys = sum(result.keys())
        for i in result.keys():
            person = dict()
            person['name'] = result[i]['name']
            score = round((1 - 1 / (1+math.exp(-4*(i-0.6)))) * 100, 2)
            if score > 91.00:
                score = 100.00
            person['score'] = score
            persons.append(person)
        data['persons'] = persons
        return Response(json.dumps(data), status=status.HTTP_200_OK)
