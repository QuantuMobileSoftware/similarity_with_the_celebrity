from bs4 import BeautifulSoup
import requests
import urllib
import os
import face_recognition

from face_recognition_part import get_face_encodings
from person.models import Person, Face
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        for num in range(0, 1): # 1800
            number_of_page = str(1 + num*50)
            r = requests.get("http://www.imdb.com/search/name?gender=male,female&ref_=nv_cel_m_3&start="+number_of_page)
            data = r.text
            soup = BeautifulSoup(data)
            for page_link in soup.find_all("td", class_="image"):
                url = page_link.find('a').get('href')
                page = requests.get("http://www.imdb.com/" + url)
                data = page.text
                soup = BeautifulSoup(data)
                image_link = soup.find("div", class_="image").find('a').find('img').get('src')
                name = soup.find("h1", class_="header").find('span').text
                img = urllib.urlretrieve(image_link)
                img = face_recognition.api.load_image_file(os.path.join(img[0]))
        
                face_encoding = get_face_encodings(img)
                if len(face_encoding) == 1:
                    person_id = Person.objects.create(name=name)
                    face_encoding = str(face_encoding[0].tolist())[1:-1]
                    Face.objects.create(person=person_id, encoding=face_encoding)



# import os
# import face_recognition
#
# from face_recognition_part import get_face_encodings
# from person.models import Person, Face
# from django.core.management.base import BaseCommand, CommandError
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         root_dir = './Photos'
#         for dir in os.listdir(root_dir):
#             person_id = Person.objects.create(name=dir)
#             for file in os.listdir(os.path.join(root_dir, dir)):
#                 if file.endswith(('jpg', 'png')):
#                     img = face_recognition.api.load_image_file(os.path.join(root_dir, dir, file))
#                     face_encoding = get_face_encodings(img)
#                     if len(face_encoding) == 1:
#                         face_encoding = str(face_encoding[0].tolist())[1:-1]
#                         Face.objects.create(person=person_id, encoding=face_encoding)
