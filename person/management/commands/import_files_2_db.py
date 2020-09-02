import requests
import urllib
import os
import logging
from multiprocessing.pool import ThreadPool as Pool

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import face_recognition
from face_recognition_part import get_face_encodings
from person.models import Person


class Command(BaseCommand):
    logger = logging.getLogger(__name__)
    i = 0

    def handle(self, *args, **options):

        def process_page(num):
            number_of_page = str(1 + num*50)
            r = requests.get("http://www.imdb.com/search/name?gender=male,female&ref_=nv_cel_m_3&start="+number_of_page)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
            for lister_item in soup.find_all("div", class_="lister-item"):
                url = lister_item.find("h3", class_="lister-item-header").find('a').get('href')
                full_url = "http://www.imdb.com/" + url

                name = lister_item.find("h3", class_="lister-item-header").find('a').text

                image_link = lister_item.find('img').get('src')
                img = urllib.urlretrieve(image_link)
                img = face_recognition.api.load_image_file(os.path.join(img[0]))
                face_encoding = get_face_encodings(img)

                if len(face_encoding) == 1:
                    face_encoding = str(face_encoding[0].tolist())[1:-1]
                    with transaction.atomic():
                        try:
                            obj = Person.objects.get(url=full_url)
                            obj.name = name
                            obj.image_link = image_link
                            obj.face_encoding = face_encoding
                            obj.save()
                        except Person.DoesNotExist:
                            Person.objects.create(url=full_url, name=name, image_link=image_link, face_encoding=face_encoding)
                            self.i += 1
                            self.logger.debug("%d persons created", self.i)

        pool_size = 20
        pool = Pool(pool_size)
        for num in range(0, 1):
            pool.apply_async(process_page, (num,))
        pool.close()
        pool.join()
