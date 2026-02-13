from django.contrib import admin
from .models import Team, Player, Match


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1
    
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'manager', 'created_at')
    search_fields = ('name', 'city')
    list_filter = ('city',)
    inlines = [PlayerInline]

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'number', 'is_injured')
    search_fields = ('first_name', 'last_name')
    list_filter = ('team', 'position', 'is_injured')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date', 'home_score', 'away_score')
    list_filter = ('match_date',)
    date_hierarchy = 'match_date'
