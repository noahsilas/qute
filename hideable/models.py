from django.db import models
from django.utils.timezone import now

class HideableManager(models.Manager):
    """A default manager that adds .active() and .hidden() filters"""
    use_for_related_fields = True

    class QuerySet(models.query.QuerySet):
        "A queryset with .active() and .hidden() filters"

        def active(self):
            "Only return active instances"
            return self.filter(deleted_at=None)

        def hidden(self):
            "Only return hidden instances"
            return self.filter(deleted_at__ne=None)

    def get_query_set(self):
        return HideableManager.QuerySet(self.model, using=self._db)

    def active(self):
        return self.get_query_set().active()

    def hidden(self):
        return self.get_query_set().hidden()


class Hideable(models.Model):
    created_at = models.DateTimeField(default=now, editable=False)
    altered_at = models.DateTimeField(editable=False)
    deleted_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    objects = HideableManager()

    def hide(self):
        self.deleted_at = now()
        self.save()

    def save(self, *args, **kwargs):
        self.altered_at = now()
        super(Hideable, self).save(*args, **kwargs)

