from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from fetch.models import Shorturl
from fetch.serializers import Shorturlserializer
from fetch.utils import validateUrl, hashCode

bad_data = {
    'status': 'FAILED',
    'status_codes': [
        'BAD_DATA'
    ]
}


@csrf_exempt
def shortUrl(request):
    data = {}

    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        long_url = requestData['long_url']
        if validateUrl(long_url):
            requestData['short_url'] = hashCode()
            newUrl = Shorturlserializer(data = requestData)
            if newUrl.is_valid():
                newUrl.save()
                ret = {
                    "short_url": 'http://'+request.META['HTTP_HOST']+'/'+requestData['short_url']+'/',
                    "status": "OK",
                    "status_codes": []
                    
                }
                return JsonResponse(ret, status = 200)
        else:
            data = {
                "status": "FAILED",
                "status_codes": ["INVALID_URLS"]
            }
    else:
        data = bad_data

    return JsonResponse(data, status = 400)


@csrf_exempt
def cleanUrls(request):
    Shorturl.objects.all().delete()
    return JsonResponse({}, status = 200)

@csrf_exempt
def redirectUrl(request, short_url):
    url = get_object_or_404(Shorturl, short_url = short_url)
    url.count = url.count+1
    url.save()
    return HttpResponseRedirect(url.long_url)

@csrf_exempt
def longUrl(request):
    data = {}
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        url = requestData['short_url']
        splitUrl = url.split('/')
        ur = []
        for tt in splitUrl:
            if tt != '' and tt != 'http:' and tt != 'https:':
                ur.append(tt)
        splitUrl = ur
        url = splitUrl[1]
        try:
            longUrl = Shorturl.objects.get(short_url = url)
            data = {
                "long_url": longUrl.long_url,
                "status": "OK",
                "status_codes": []
            }
        except Shorturl.DoesNotExist:
            data = {
                "status": "FAILED",
                "status_codes": ["SHORT_URLS_NOT_FOUND"]
            }
        return JsonResponse(data, status = 200)
    else:
        data = bad_data
    return JsonResponse(data, status = 400)


@csrf_exempt
def countUrl(request):
    data = {}
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        url = requestData['short_url']
        splitUrl = url.split('/')
        ur = []
        for tt in splitUrl:
            if tt != '' and tt != 'http:' and tt != 'https:':
                ur.append(tt)
        splitUrl = ur
        url = splitUrl[1]
        try:
            shortUrl = Shorturl.objects.get(short_url = url)
            data = {
                "count": shortUrl.count,
                "status": "OK",
                "status_codes": []
            }
        except Shorturl.DoesNotExist:
            data = {
                "status": "FAILED",
                "status_codes": ["SHORT_URLS_NOT_FOUND"]
            }
        return JsonResponse(data, status = 200)
    else:
        data = bad_data
    return JsonResponse(data, status = 400)