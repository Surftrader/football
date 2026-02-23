from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Team, Player, Match

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'city', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва команди'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місто'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'position', 'number', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'match_date', 'stadium', 'home_score', 'away_score']
        widgets = {
            'match_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'stadium': forms.TextInput(attrs={'class': 'form-control'}),
            'home_team': forms.Select(attrs={'class': 'form-select'}),
            'away_team': forms.Select(attrs={'class': 'form-select'}),
            'home_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'away_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            user_teams = Team.objects.filter(manager=user)
            self.fields['home_team'].queryset = user_teams
            self.fields['away_team'].queryset = user_teams

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get('home_team')
        away_team = cleaned_data.get('away_team')
        match_date = cleaned_data.get('match_date')

        if home_team and away_team and home_team == away_team:
            raise ValidationError("Домашня та гостьова команди не можуть бути однаковими.")
        
        if not self.instance.pk and match_date is not None:
            if match_date < timezone.now():
                raise ValidationError("Дата запланованого матчу не може бути в минулому.")
        return cleaned_data
    