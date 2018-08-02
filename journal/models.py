# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Resource(models.Model):
    # Create your models here.
    name = models.CharField(max_length=200)
    link = models.URLField(default=None)

    def __str__(self):
        return self.name

    def full_description(self):
        return self.name + self.link