from django.conf.urls import patterns, include, url

from .views import ProjectList


urlpatterns = patterns('project.views',
    url(r'^$', ProjectList.as_view(), name='projects'),
)
