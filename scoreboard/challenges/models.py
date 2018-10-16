from __future__ import unicode_literals

import collections
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.crypto import constant_time_compare


class Challenge(models.Model):

    class Meta:
        ordering = ['points', 'name']

    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    points = models.IntegerField()
    port = models.IntegerField()
    description = models.TextField()
    flag = models.CharField(max_length=128)
    solved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    instructions = models.CharField(max_length=64, blank=True, null=True)

    def check_flag(self, user, flag):
        if not user.is_authenticated():
            return 'Please authenticate.'

        expected = self.flag.lower()
        provided = flag.strip().lower()
        if constant_time_compare(expected, provided):
            self.solved.add(user)
            return 'Correct!'
        else:
            return 'Incorrect flag :-('

    @classmethod
    def solved_by_user(cls, user):
        if user.is_authenticated():
            solved = cls.objects.filter(solved=user).values('pk', 'points')
            total_points = sum(challenge['points'] for challenge in solved)
            ids = set(challenge['pk'] for challenge in solved)
            return ids, total_points
        else:
            return set(), 0

    @classmethod
    def all_by_category(cls):
        challenges = cls.objects.all()
        output = collections.OrderedDict()
        for challenge in challenges:
            # FIXME: make this a field on the model
            category = challenge.name.split('-', 1)[0]
            try:
                output[category].append(challenge)
            except KeyError:
                output[category] = [challenge]
        return output

    def __str__(self):
        return 'Challenge: {}'.format(self.name)


class AutoUserManager(BaseUserManager):

    def create_user(self, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance

    def create_superuser(self, **kwargs):
        return self.create_user(is_superuser=True)


class AutoUser(AbstractBaseUser):

    objects = AutoUserManager()

    USERNAME_FIELD = 'user_id'

    user_id = models.CharField(max_length=36, unique=True)

    # Django Admin support
    is_superuser = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        user_id = str(uuid.uuid4())
        super().__init__(user_id=user_id, *args, **kwargs)

    def __str__(self):
        return 'user_%d' % (self.id,)

    # Django admin support

    def __repr__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

    def get_short_name(self):
        return str(self)

