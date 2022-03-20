from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm


class Signup(CreateView):
    form_class = SignupForm
    template_name = 'custom_user/register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect()
