from __future__ import unicode_literals

import collections
import uuid

from django.conf import settings
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
    category = models.CharField(max_length=64, blank=True, null=True)

    def check_flag(self, session, flag):
        """ Check a flag and store the result if it's correct.
        """
        solved = session.get('solved', [])
        primary_key = self.id
        if self.flag_is_correct(flag):
            if primary_key not in solved:
                session['solved'] = solved + [primary_key]
            return 'Correct!'
        else:
            return 'Incorrect flag :-('

    def flag_is_correct(self, flag):
        """ Test if a flag matches the challenge metadata.
        """
        expected = self.flag.lower()
        provided = flag.strip().lower()
        wrapped = 'flag{%s}' % (provided,)
        if constant_time_compare(expected, provided) or \
                constant_time_compare(expected, wrapped):
            return True
        else:
            return False

    @classmethod
    def total_points(cls, solved):
        """ Calculate the total points for a user.
        """
        correct = cls.objects.filter(id__in=solved).values('points')
        total_points = sum(challenge['points'] for challenge in correct)
        return total_points

    def __str__(self):
        return 'Challenge: {}'.format(self.name)

