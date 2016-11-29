from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'jplace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #browsing
    url(r'^$', 'jplaceapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^save/$', 'jplaceapp.views.testimonies_save_page', name='testimonies_save_page'),
    url(r'^testimonies/(\d+)/$', 'jplaceapp.views.testimonies_page', name='testimonies_page'),
    url(r'^tag/$', 'jplaceapp.views.tag_cloud_page', name='tag_cloud_page'),
    url(r'^search/$','jplaceapp.views.search_page', name='search_page'),
    url(r'^popular/$', 'jplaceapp.views.popular_page', name='popular_page'),
    url(r'^user/testimony/(?P<id>\d+)/$', 'jplaceapp.views.testimony_detail', name='testimony_detail'),
    #user
    url(r'^user/(\w+)/$', 'jplaceapp.views.user_page', name='user_page'),
    url(r'^tag/([^\s]+)/$','jplaceapp.views.tag_page', name='tag_page'),
    url(r'^vote/$', 'jplaceapp.views.testimony_vote_page', name='testimony_vote_page'),
    url(r'^comments/', include('django_comments.urls')),
    #user registration
    url(r'^accounts/', include('registration.backends.default.urls')),
    #friends
    url(r'^friends/(\w+)/$', 'jplaceapp.views.friends_page', name='friends_page'),
    url(r'^friend/add/$', 'jplaceapp.views.friend_add', name='friend_add'),
    url(r'^friend/invite/$', 'jplaceapp.views.friend_invite', name='friend_invite'),
    url(r'^friend/accept/(\w+)/$', 'jplaceapp.views.friend_accept', name='friend_accept'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)