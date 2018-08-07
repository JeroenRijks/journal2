# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length = 200)

    # def get_related_resources(self):
    #     return Resource.objects.filter(Tag__contains=self)
    # THIS IS THE MORE EFFICIENT TAG-LIST LIST OF RELATED RESOURCES

    def __str__(self):
        return self.name


class Resource(models.Model):
    # Create your models here.
    name = models.CharField(max_length=200)
    link = models.URLField(default=None)
    tip = models.CharField(max_length=2048, default=None)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def full_description(self):
        return self.name + self.link

    @staticmethod
    def say_hello():
        return "hello world"