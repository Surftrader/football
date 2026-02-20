from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import TeamForm, PlayerForm
from .models import Team, Player


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/index.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        return Team.objects.filter(manager=self.request.user)


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.manager = self.request.user
        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('index')
    
    def get_queryset(self):
        return Team.objects.filter(manager=self.request.user)
    

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('index')
    
    def get_queryset(self):
        return Team.objects.filter(manager=self.request.user)


class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'teams/player_list.html'
    context_object_name = 'players'
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        self.team = get_object_or_404(Team, id=team_id, manager=self.request.user)
        return Player.objects.filter(team=self.team)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.team
        return context


class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'teams/player_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs.get('team_id')
        context['team'] = get_object_or_404(Team, id=team_id, manager=self.request.user)
        return context
    
    def form_valid(self, form):
        team_id = self.kwargs.get('team_id')
        team = get_object_or_404(Team, id=team_id, manager=self.request.user)
        form.instance.team = team
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('player_list', kwargs={'team_id': self.kwargs.get('team_id')})
