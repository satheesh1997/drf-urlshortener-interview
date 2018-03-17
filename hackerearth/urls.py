from django.contrib import admin
from django.urls import path, re_path
from fetch.views import shortUrl, cleanUrls, longUrl, redirectUrl, countUrl, shortUrls, longUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fetch/short-url/', shortUrl),
    path('fetch/short-urls/', shortUrls),
    path('fetch/long-url/', longUrl),
    path('fetch/long-urls/', longUrls),
    path('fetch/count/', countUrl),
    path('clean-urls/', cleanUrls),
    re_path(r'^(?P<short_url>[\w-]+)/$', redirectUrl),
]
