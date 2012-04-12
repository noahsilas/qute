from django.db.models.aggregates import Sum
from django.db.models.sql.aggregates import Sum as SumAggregate

class DefaultAggregate(SumAggregate):
    """ When summing no rows, databases may return null instead of zero.
        Use this to supply a default value (usually zero) to be used in
        its place. """
    sql_template = 'COALESCE(%(function)s(%(field)s), %(default)s)'

class DefaultSum(Sum):
    """ When summing no rows, databases may return null instead of zero.
        Use this to supply a default value (usually zero) to be used in
        its place. """
    name = "DefaultSum"

    def add_to_query(self, query, alias, col, source, is_summary):
        params = {'default': 0}
        params.update(self.extra)
        query.aggregates[alias] = DefaultAggregate(
            col,
            source=source,
            is_summary=is_summary,
            **params
        )


