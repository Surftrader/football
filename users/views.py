from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import ManagerRegistrationForm

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = ManagerRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Here you can automatically log in a user after registration:
        # login(self.request, self.object)
        return response
