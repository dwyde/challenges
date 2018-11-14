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
    category = models.CharField(max_length=64, blank=True, null=True)

    def check_flag(self, user, flag):
        if not user.is_authenticated:
            return 'Please authenticate.'

        expected = self.flag.lower()
        provided = flag.strip().lower()
        wrapped = 'flag{%s}' % (provided,)
        if constant_time_compare(expected, provided) or \
                constant_time_compare(expected, wrapped):
            self.solved.add(user)
            return 'Correct!'
        else:
            return 'Incorrect flag :-('

    @classmethod
    def solved_by_user(cls, user):
        if user.is_authenticated:
            solved = cls.objects.filter(solved=user).values('pk', 'points')
            total_points = sum(challenge['points'] for challenge in solved)
            ids = set(challenge['pk'] for challenge in solved)
            return ids, total_points
        else:
            return set(), 0

    def __str__(self):
        return 'Challenge: {}'.format(self.name)


class AutoUserManager(BaseUserManager):

    def create_user(self, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance


class AutoUser(AbstractBaseUser):

    objects = AutoUserManager()

    USERNAME_FIELD = 'id'

    def __str__(self):
        return 'user_%d' % (self.id,)

