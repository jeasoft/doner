from django.views.generic.list import ListView

from .models import Project


class ProjectList(ListView):

    model = Project
