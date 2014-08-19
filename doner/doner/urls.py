from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'doner.views.logout_view', name='logout'),
    url(r'', include('project.urls')),
)
