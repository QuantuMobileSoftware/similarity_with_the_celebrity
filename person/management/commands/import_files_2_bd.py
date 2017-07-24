import os
import face_recognition

from face_recognition_part import get_face_encodings
from person.models import Person, Face
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        root_dir = './Photos'
        for dir in os.listdir(root_dir):
            person_id = Person.objects.create(name=dir)
            for file in os.listdir(os.path.join(root_dir, dir)):
                if file.endswith(('jpg', 'png')):
                    img = face_recognition.api.load_image_file(os.path.join(root_dir, dir, file))
                    face_encoding = get_face_encodings(img)
                    if len(face_encoding) == 1:
                        face_encoding = str(face_encoding[0].tolist())[1:-1]
                        Face.objects.create(person=person_id, encoding=face_encoding)
