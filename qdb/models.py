from django.db import models
from hideable.models import Hideable, HideableManager

class QuoteManager(HideableManager):
    class QuerySet(HideableManager.QuerySet):
        def with_score(self):
            "Annotates this QS with the voting score"
            return self.annotate(score=models.Sum('vote__score'))

    def get_query_set(self):
        return QuoteManager.QuerySet(self.model, using=self._db)

    def with_score(self):
        return self.get_query_set().with_score()


class Quote(Hideable, models.Model):
    body = models.TextField()
    ip = models.GenericIPAddressField()

    objects = QuoteManager()


class Vote(Hideable, models.Model):
    ip = models.GenericIPAddressField()
    quote = models.ForeignKey(Quote)
    score = models.SmallIntegerField()

