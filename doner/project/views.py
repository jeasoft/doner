# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext as _
from django.conf import settings

from .access_control_views import (
    LoginRequiredView, SuperUserView, ProjectView, MembersOnlyView, UserPrivateView
)
from .models import Project, Ticket, Log


class ProjectList(ListView):

    model = Project


class ProjectCreate(SuperUserView, CreateView):

    model = Project
    fields = ['name', 'description', 'is_private', 'members']


class ProjectEdit(SuperUserView, UpdateView):

    model = Project
    fields = ['name', 'description', 'is_private', 'members']


class ProjectActivity(ProjectView, TemplateView):

    template_name = "project/project-activity.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectActivity, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['new_tickets'] = Ticket.objects.all().order_by('-id')[:10]
        context['last_log'] = Log.objects.all().order_by('-id')[:10]
        return context


class Tickets(ProjectView, ListView):

    model = Ticket
    template_name = 'project/tickets.html'
    ordering_fields = ('title', 'status', 'ttype', 'submitted_date', 'modified_date')

    def get_queryset(self):
        queryset = self.model.objects.filter(project__id=self.kwargs['pk'])

        filter_by = self.request.GET.get('filter')
        if filter_by and filter_by in ('closed'):
            queryset = queryset.filter(status=3)
        else:
            queryset = queryset.filter(status__lt=3)

        order = self.request.GET.get('order')
        if order in self.ordering_fields:
            queryset = queryset.order_by(order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(Tickets, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        context['order'] = self.request.GET.get('order')
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context


class TicketDetails(ProjectView, DetailView):

    model = Ticket
    url_pk_related_model = Ticket
    template_name = 'project/ticket.html'


class TicketForm(View):

    model = Ticket
    fields = ['title', 'description', 'status', 'priority', 'ttype', 'assigned_to']


class TicketCreate(TicketForm, MembersOnlyView, CreateView):

    def get_form(self, form_class):
        '''
        Restrict available choices in 'assigned_to' field to project members.
        '''
        form = super(TicketCreate, self).get_form(form_class)
        self.get_project()
        form.fields['assigned_to'].queryset = self.project.members.all()
        return form

    def form_valid(self, form):
        '''
        Setting project and submitter fields before saving the form.
        '''
        self.get_project()
        form.instance.project = self.project
        form.instance.submitter = self.request.user
        return super(TicketCreate, self).form_valid(form)


class TicketEdit(TicketForm, MembersOnlyView, UpdateView):

    url_pk_related_model = Ticket

    def form_valid(self, form):
        '''
        Adding event to ticket log.
        '''
        CHOICES_FIELDS = ['status', 'priority', 'ttype']
        TEXT_FIELDS = ['description']
        FOREIGN_KEY_FIELDS = ['assigned_to']

        self.ticket = form.instance

        if form.changed_data:
            lines = []
            for field_name in form.changed_data:
                form_field = form.fields[field_name]
                field_initial = form.initial[field_name]
                field_current = form.data[field_name]
                if field_name in CHOICES_FIELDS:
                    # getting display values
                    choices = dict(form_field.choices)
                    initial_value = choices[int(field_initial)].title()
                    current_value = choices[int(field_current)].title()
                elif field_name in TEXT_FIELDS:
                    # no tracking details of content changes
                    initial_value = _('updated')
                    current_value = ''
                elif field_name in FOREIGN_KEY_FIELDS:
                    # foreign key values
                    choices = dict(form_field.choices)
                    initial_value = choices[int(field_initial)] if field_initial else u'—'
                    current_value = choices[int(field_current)] if field_current else u'—'
                else:
                    # raw values
                    initial_value = field_initial
                    current_value = field_current

                # format log message
                if current_value:
                    current_value = u' ⇒ %s' % current_value
                lines.append(u'{0}: {1}{2}'.format(
                    form_field.label.title(),
                    initial_value,
                    current_value
                ))

            # create log entry
            self.ticket.log_set.create(
                author=self.request.user,
                description='\n'.join(lines)
            )

        return super(TicketEdit, self).form_valid(form)


class CommentAdd(MembersOnlyView, CreateView):

    model = Log
    url_pk_related_model = Ticket
    fields = ['description']

    def form_valid(self, form):
        '''
        Setting ticket and submitter fields before saving the form.
        '''
        self.ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        form.instance.ticket = self.ticket
        form.instance.author = self.request.user
        form.instance.ltype = 2

        return super(CommentAdd, self).form_valid(form)

    def get_success_url(self):
        return self.ticket.get_absolute_url()


class MyTickets(ListView):

    model = Ticket
    template_name = 'project/my_tickets.html'
    ordering_fields = ('title', 'status', 'ttype', 'submitted_date', 'modified_date')

    def get_queryset(self):

        queryset = self.model.objects.filter(assigned_to=self.request.user)

        filter_by = self.request.GET.get('filter')
        if filter_by and filter_by in ('closed'):
            queryset = queryset.filter(status=3)
        else:
            queryset = queryset.filter(status__lt=3)

        order = self.request.GET.get('order')
        if order in self.ordering_fields:
            queryset = queryset.order_by(order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyTickets, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        context['order'] = self.request.GET.get('order')
        return context
