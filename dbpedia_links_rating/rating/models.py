# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from dbpedia_links_rating.users.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from random import randint
from django.db.models.aggregates import Count


@python_2_unicode_compatible
class Link(models.Model):
    subject = models.CharField(max_length=200)
    object = models.CharField(max_length=200)
    predicate = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.subject + " -- " + self.predicate + " -- " + self.object + " -- " + str(self.score)

    def randomComplete(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def randomNotRated(self):
        """
        TODO
        :return:
        """


@python_2_unicode_compatible
class Rating(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    RATING = (
        (-1, 'No'),
        (0, 'Unsure'),
        (1, 'Yes'),
    )
    rating = models.IntegerField(default=0, choices=RATING)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __int__(self):
        return self.rating


@python_2_unicode_compatible
class File(models.Model):
    file = models.FileField(upload_to='links/%Y/%m/%d')
