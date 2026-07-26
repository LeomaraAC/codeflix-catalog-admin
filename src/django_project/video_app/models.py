from uuid import uuid4

from django.db import models

from src.core.video.domain.value_objects import Rating

class Video(models.Model):
    app_label = 'video_app'

    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    published = models.BooleanField(default=False)
    rating = models.CharField(max_length=20, choices=[(tag.name, tag.name) for tag in Rating])
    categories = models.ManyToManyField('category_app.Category', related_name='videos')
    genres = models.ManyToManyField('genre_app.Genre', related_name='videos')
    cast_members = models.ManyToManyField('cast_member_app.CastMember', related_name='videos')
    
    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.title
