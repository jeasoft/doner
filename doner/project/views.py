from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Project, Ticket


class ProtectedView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class ProjectList(ListView):
    model = Project


class Tickets(ListView):
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


class TicketDetails(DetailView):
    model = Ticket
    template_name = 'project/ticket.html'
