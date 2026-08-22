from django.contrib import admin

from src.django_project.video_app.models import AudioVideoMedia, ImageMedia, Video


admin.site.register(Video)
admin.site.register(ImageMedia)
admin.site.register(AudioVideoMedia)
