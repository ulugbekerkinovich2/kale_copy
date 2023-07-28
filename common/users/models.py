import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta
from common.users.managers import UserManager
from common.users.validator import PhoneNumberValidator


class GENDER(models.IntegerChoices):
    MALE = 1, "MALE"
    FEMALE = 2, "FEMALE"


class User(AbstractUser, BaseModel):
    class UserRole(models.IntegerChoices):
        ADMIN = 1, "ADMIN"
        CLIENT = 2, "CLIENT"

    first_name = None
    last_name = None
    username = models.CharField(max_length=15, null=True, blank=True)

    phone_validator = PhoneNumberValidator()

    name = models.CharField(_("Name of User"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20, unique=True,
                             help_text=_("Required. 13 characters or fewer."),
                             validators=[phone_validator],
                             error_messages={"unique": _("A user with that phone already exists."), })
    gender = models.IntegerField(_("Gender"), choices=GENDER.choices, null=True, blank=True)
    photo = models.ImageField(_("Image of User"), upload_to='userImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})
    region = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)

    role = models.IntegerField(_("Role"), choices=UserRole.choices, default=UserRole.CLIENT)
    is_verified = models.BooleanField(_("Is verified"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return "USER:" + ' ' + str(self.phone)


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return f"{self.number}"

    def generate_code(self, *args, **kwargs):
        number_list = list(range(10))
        code_items = ''
        for _ in range(5):
            code_items += str(random.choice(number_list))
        self.number = code_items
        self.save()
        return self.number
