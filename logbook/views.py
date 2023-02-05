from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import LogbookForm
from .models import Logbook


class LogbookListView(UserPassesTestMixin, ListView):
    model = Logbook
    template_name = 'logbook_list.html'
    context_object_name = 'logbooks'

    def test_func(self):
        return self.request.user.has_perm('logbook.view_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')


class LogbookDetailView(DetailView):
    model = Logbook
    template_name = 'logbook_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LogbookCreateView(CreateView):
    model = Logbook
    form_class = LogbookForm
    template_name = 'logbook_form.html'
    success_url = reverse_lazy('logbook:logbook-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LogbookUpdateView(UpdateView):
    model = Logbook
    form_class = LogbookForm
    template_name = 'logbook_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class LogbookDeleteView(DeleteView):
    model = Logbook
    template_name = 'logbook_confirm_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def get_success_url(self):
        return reverse('schedule:lesson-list')
