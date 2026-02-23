from django.urls import path
from .views import TeamListView, TeamCreateView, TeamUpdateView, \
    TeamDeleteView, PlayerListView, PlayerCreateView, PlayerUpdateView, \
        PlayerDeleteView, MatchListView, MatchCreateView

urlpatterns = [
    path('', TeamListView.as_view(), name='index'),
    path('teams/create/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/update/', TeamUpdateView.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    path('teams/<int:team_id>/players/', PlayerListView.as_view(), name='player_list'),
    path('teams/<int:team_id>/players/add/', PlayerCreateView.as_view(), name='player_create'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player_edit'),
    path('players/<int:pk>/delete/', PlayerDeleteView.as_view(), name='player_delete'),
    path('matches/', MatchListView.as_view(), name='match_list'),
    path('matches/add/', MatchCreateView.as_view(), name='match_create'),
]
