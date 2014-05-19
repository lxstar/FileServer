from django.conf.urls import patterns, include, url

urlpatterns = patterns('upload.views',
            (r'^$', 'index'),
)
