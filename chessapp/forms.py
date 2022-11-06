from django import forms
from .models import Partie


class GameForm(forms.ModelForm):

    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.fields['user'].disabled = True

    class Meta:
        model = Partie
        fields = ["user", "nazwa", "PGN", "FEN"]
        labels = {'nazwa': "Nazwa", "PGN": "PGN", "FEN": "FEN"}
