from lzma import MODE_FAST
from django.contrib import admin

from .models import Theater, Movie, MovieViewingEvent

admin.site.register(Theater)
admin.site.register(Movie)
admin.site.register(MovieViewingEvent)