from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel


class News(BaseModel):
    title = models.CharField(max_length=250)
    description = RichTextField()
    videoURL = models.URLField(null=True, blank=True)
    photo = models.ImageField(_("Image of News"), upload_to='newsImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(966, 627)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(322, 209)], format='PNG',
                                 options={'quality': 70})

    def __str__(self):
        return self.title
