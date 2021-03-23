from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.gis.geos import Point


# Create your models here. pnt = Point(5, 23)

class Target(models.Model):
    coord = models.PointField(default=Point(0.0, 0.0, 0.0), dim=3)
    name = models.CharField(max_length=200)


class Observation(models.Model):
    image = models.ImageField(upload_to=settings.IMG_URL, default=None)
    timestamp = models.DateTimeField(auto_now_add=False)
    name = models.CharField(max_length=200, default="")
