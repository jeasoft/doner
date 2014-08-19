from django.conf.urls import patterns, include, url

from .views import ProjectList, Tickets, TicketDetails


urlpatterns = patterns('project.views',
    url(r'^$', ProjectList.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)/$', Tickets.as_view(), name='project'),
    url(r'^ticket/(?P<pk>\d+)/$', TicketDetails.as_view(), name='ticket'),
)
