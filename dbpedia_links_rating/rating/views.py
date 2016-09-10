# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Link, UserRating

class RatingView(LoginRequiredMixin, TemplateView):
    template_name = 'rating/rating_link.html'

