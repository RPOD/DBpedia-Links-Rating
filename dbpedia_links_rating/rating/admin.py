from django.contrib import admin

from .models import Link, UserRating, File

admin.site.register(Link)
admin.site.register(UserRating)
admin.site.register(File)
