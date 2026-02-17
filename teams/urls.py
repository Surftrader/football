from django.urls import path
from .views import TeamListView, TeamCreateView, TeamUpdateView, TeamDeleteView

urlpatterns = [
    path('', TeamListView.as_view(), name='index'),
    path('teams/create/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/update/', TeamUpdateView.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
]
