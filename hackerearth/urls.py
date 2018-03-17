from django.contrib import admin
from django.urls import path, re_path
from fetch.views import shortUrl, cleanUrls, longUrl, redirectUrl, countUrl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fetch/short-url/', shortUrl),
    path('fetch/long-url/', longUrl),
    path('fetch/count/', countUrl),
    path('clean-urls/', cleanUrls),
    re_path(r'^(?P<short_url>[\w-]+)/$', redirectUrl),
]
