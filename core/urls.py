from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from home.views import PostListTileView, PostListFeedView, AboutView


urlpatterns = [
    url(r'^$', PostListTileView.as_view(), name='home'),
    url(r'^posts/$', PostListFeedView.as_view(), name='home_list'),

    url(r'^tags/$', TemplateView.as_view(template_name='home/tags.html'), name='tags'),
    url(r'^links/$', TemplateView.as_view(template_name='home/links.html'), name='links'),
    url(r'^about/$', AboutView.as_view(), name='about'),

    url(r'^djadmin/', include(admin.site.urls)),
    url(r'^wagadmin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/$', 'search.views.search', name='search'),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('img/favicon.ico'),
                                                permanent=True)),
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
