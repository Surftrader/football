from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from datetime import date

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_teams'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


def validate_age(value):
    if value:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if value > today:
            raise ValidationError("Дата народження не може бути у майбутньому.")   
        if age < 5 or age > 60:
            raise ValidationError(f"Некоректний вік ({age} років). Дозволено від 5 до 60 років.")


class Player(models.Model):
    POSITIONS = [
        ('GK', 'Воротар'),
        ('DF', 'Захисник'),
        ('MF', 'Півзахисник'),
        ('FW', 'Нападник'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=2, choices=POSITIONS, default='GK')
    number = models.PositiveIntegerField()
    birth_date = models.DateField(null=True, blank=True, validators=[validate_age])
    is_injured = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.team.name})"


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateTimeField()
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    stadium = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.match_date.strftime('%Y-%m-%d')}"
    
