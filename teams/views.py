from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Team


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/index.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        return Team.objects.filter(manager=self.request.user)
