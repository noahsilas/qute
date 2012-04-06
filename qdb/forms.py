from django.forms import ModelForm
from qdb.models import Vote, Quote

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        exclude = ('ip',)


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        exclude = ('ip',)
