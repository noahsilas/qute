from django.db import models
from django.core.exceptions import ValidationError
from hideable.models import Hideable, HideableManager

class QuoteManager(HideableManager):
    class QuerySet(HideableManager.QuerySet):
        def with_scores(self):
            "Annotates this QS with the voting score"
            return self.annotate(score=models.Sum('vote__score'))

    def get_query_set(self):
        return QuoteManager.QuerySet(self.model, using=self._db)

    def with_scores(self):
        return self.get_query_set().with_scores()


class Quote(Hideable, models.Model):
    body = models.TextField()
    ip = models.GenericIPAddressField()

    objects = QuoteManager()

    def get_score(self, refresh=False):
        if hasattr(self, 'score') and not refresh:
            return self.score
        q = Quote.objects.with_scores().get(pk=self.pk)
        self.score = q.score
        return self.score


def check_score(score):
    if abs(score) > 1:
        raise ValidationError("Score must be in range [-1,1]")

class Vote(Hideable, models.Model):
    ip = models.GenericIPAddressField()
    quote = models.ForeignKey(Quote)
    score = models.SmallIntegerField(validators=[check_score])
