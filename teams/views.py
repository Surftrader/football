from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import TeamForm, PlayerForm, MatchForm
from .models import Team, Player, Match


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

    def dispatch(self, request, *args, **kwargs):
        team = Team.objects.filter(pk=self.kwargs.get('pk'), manager=request.user).first()

        if not team:
            storage = messages.get_messages(request)
            storage.used = True
            
            messages.error(request, "Команду не знайдено або у вас немає прав на її видалення.")
            return redirect('index')

        self.object = team
        return super().dispatch(request, *args, **kwargs)
    
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


class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'teams/player_form.html'
    
    def get_queryset(self):
        return Player.objects.filter(team__manager=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.object.team
        return context
    
    def get_success_url(self):
        return reverse_lazy('player_list', kwargs={'team_id': self.object.team.id})


class PlayerDeleteView(LoginRequiredMixin, DeleteView):
    model = Player
    template_name = 'teams/player_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        player = Player.objects.filter(pk=self.kwargs.get('pk'), team__manager=request.user).first()

        if not player:
            messages.error(request, "Гравця не знайдено або у вас немає прав на його видалення.")
            return redirect('index')

        self.object = player
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('player_list', kwargs={'team_id': self.object.team.id})
    


class MatchListView(LoginRequiredMixin, ListView):
    model = Match
    template_name = 'teams/match_list.html'
    context_object_name = 'matches'
    
    def get_queryset(self):
        user_teams = Team.objects.filter(manager=self.request.user)
        return Match.objects.filter(
                Q(home_team__in=user_teams) | Q(away_team__in=user_teams)
            ).order_by('-match_date')


class MatchCreateView(LoginRequiredMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'teams/match_form.html'
    success_url = reverse_lazy('match_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

