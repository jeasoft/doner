from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .access_control_views import SuperUserView, ProjectView, MembersOnlyView
from .models import Project, Ticket


class ProjectList(ListView):

    model = Project


class ProjectCreate(SuperUserView, CreateView):

    model = Project
    fields = ['name', 'description', 'is_private', 'members']


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
