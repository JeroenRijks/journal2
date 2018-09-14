# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def get_related_resources(self):
        return Resource.objects.filter(tags=self)

    def __str__(self):
        return self.name

class Resource(models.Model):
    # Create your models here.
    name = models.CharField(max_length=200)
    link = models.URLField(default=None)
    tip = models.CharField(max_length=2048, default=None)
    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(User, related_name='creations', default=None, null=True, blank=True)
    last_updated_by = models.ForeignKey(User, related_name='updated_tips', default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def full_description(self):
        return self.name + self.link