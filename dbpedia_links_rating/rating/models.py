# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from dbpedia_links_rating.users.models import User
from django.core.files import File
from random import randint
from django.db.models.aggregates import Count


@python_2_unicode_compatible
class Link(models.Model):
    subject = models.CharField(max_length=200)
    object = models.CharField(max_length=200)
    predicate = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.subject + " -- " + self.predicate + " -- " + self.object + " -- " + str(self.rating)

    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


@python_2_unicode_compatible
class UserRating(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    USER_RATING = (
        (-1, 'No'),
        (0, 'Unsure'),
        (1, 'Yes'),
    )
    user_rating = models.IntegerField(default=0, choices=USER_RATING)

    def __int__(self):
        return self.rating

    @classmethod
    def create(cls, link, user, user_rating):
        uR = cls(link=link, user=user, user_rating=user_rating)
        cL = Link.objects.get(pk=cls.link)
        cL.rating += cls.user_rating
        cL.save()
        return uR


@python_2_unicode_compatible
class File(models.Model):
    file = models.FileField(upload_to='links/%Y/%m/%d')

    @classmethod
    def create(cls, file):
        """
        TODO: Make things work (create link entries for each line)
        :param file:
        :return:
        """
        links = cls(file=file)
        f = open(links.file.path, 'r', encoding="utf8")
        for line in f:
            link = Link(subject=line.split('>')[0].replace('<','') , predicate=line.split('>')[1].replace('<',''), object=line.split('>')[2].replace('<',''))
            link.save()
        f.close()
        return file
