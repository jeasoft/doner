from django.conf.urls import patterns, include, url

from .views import (
    ProjectList, Tickets, TicketDetails, ProjectCreate, TicketCreate,
    TicketEdit, CommentAdd, ProjectActivity
)


urlpatterns = patterns('project.views',
    url(r'^$', ProjectList.as_view(), name='projects'),
    url(r'^project/create/$', ProjectCreate.as_view(), name='project-create'),
    url(r'^project/(?P<pk>\d+)/$', Tickets.as_view(), name='project'),
    url(r'^project/(?P<pk>\d+)/create/$', TicketCreate.as_view(), name='ticket-create'),
    url(r'^project/(?P<pk>\d+)/activity/$', ProjectActivity.as_view(), name='project-activity'),
    url(r'^ticket/(?P<pk>\d+)/$', TicketDetails.as_view(), name='ticket'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', TicketEdit.as_view(), name='ticket-edit'),
    url(r'^ticket/(?P<pk>\d+)/add-comment/$', CommentAdd.as_view(), name='ticket-add-comment'),
)
