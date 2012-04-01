from django.db import models
from hideable.models import Hideable, HideableManager

class Quote(Hideable, models.Model):
    body = models.TextField()
    ip = models.GenericIPAddressField()

    def score(self):
        return self.vote_set.aggregate(models.Sum('score'))['score']


class Vote(Hideable, models.Model):
    ip = models.GenericIPAddressField()
    quote = models.ForeignKey(Quote)
    score = models.SmallIntegerField()

