from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import TeamForm
from .models import Team


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












