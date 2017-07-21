"""
Person urls module
"""
from django.conf.urls import url
from person.views import FaceListCreateAPIView

urlpatterns = [
    url(r'^$', FaceListCreateAPIView.as_view(), name='db'),
]
