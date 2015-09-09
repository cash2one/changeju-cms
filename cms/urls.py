from django.conf.urls import patterns, include, url

from django.contrib import admin
import demo
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/'}), 
    url(r'^demo/', include(demo.urls)),
)

urlpatterns += patterns('ds.views',
    url(r'^ds/index/$', 'index'),
    url(r'^ds/list/$', 'list'),
)