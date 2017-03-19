from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Challenge(models.Model):

    class Meta:
        ordering = ['points']

    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    points = models.IntegerField()
    port = models.IntegerField()
    description = models.TextField()
    flag = models.CharField(max_length=128)
    solved = models.ManyToManyField(User, blank=True)
    instructions = models.CharField(max_length=64, blank=True, null=True)

    def check_flag(self, user, flag):
        if not user.is_authenticated():
            return 'Please authenticate.'
        
        # FIXME: constant-time compare?
        if self.flag.lower() == flag.lower():
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

    def __str__(self):
        return 'Challenge: {}'.format(self.name)

