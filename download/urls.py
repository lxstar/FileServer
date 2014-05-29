from django.conf.urls import patterns, include, url

urlpatterns = patterns('download.views',
            (r'^$', 'index'),
)