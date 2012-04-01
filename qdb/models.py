from django.db import models


class Quote(models.Model):
    body = models.TextField()
    ip = models.GenericIPAddressField()

    def score(self):
        return self.vote_set.aggregate(models.Sum('score'))['score']

class Vote(models.Model):
    ip = models.GenericIPAddressField()
    quote = models.ForeignKey(Quote)
    score = models.SmallIntegerField()

