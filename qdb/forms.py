from django.forms import ModelForm
from qdb.models import Vote

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        exclude = ('ip')
