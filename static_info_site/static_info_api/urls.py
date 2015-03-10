from django.conf.urls import patterns, include, url
from views import Learn, Predict

urlpatterns = patterns('static_info_api.views',
    # Examples:
    # url(r'^$', 'senz_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^learn/$', Learn),
    url(r'^predict/$', Predict)
)