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
            try:
                shortUrl = Shorturl.objects.get(long_url = long_url)
                ret = {
                        "short_url": 'http://'+request.META['HTTP_HOST']+'/'+shortUrl.short_url+'/',
                        "status": "OK",
                        "status_codes": []
                        
                }
            except Shorturl.DoesNotExist:
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

    return JsonResponse(data, status = 404)


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
    return JsonResponse(data, status = 404)


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
    return JsonResponse(data, status = 404)


@csrf_exempt
def shortUrls(request):
    data = {}
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        invalid_urls = []
        valid_urls = {}
        long_urls = requestData['long_urls']
        for url in long_urls:
            if not validateUrl(url):
                invalid_urls.append(url)
        if len(invalid_urls) > 0:
            data =  {
                    "invalid_urls" : invalid_urls,
                    "status": "FAILED",
                    "status_codes": ["INVALID_URLS"]
                }
        else:
            for url in long_urls:
                smallurl = hashCode()
                try:
                    shortUrl = Shorturl.objects.get(long_url = url)
                    valid_urls[url] = 'http://'+request.META['HTTP_HOST']+'/'+shortUrl.short_url+'/'
                except Shorturl.DoesNotExist:
                    sd = {
                        'long_url': url,
                        'short_url': smallurl
                    }
                    newUrl = Shorturlserializer(data = sd)
                    if newUrl.is_valid():
                        newUrl.save()
                        valid_urls[url] = 'http://'+request.META['HTTP_HOST']+'/'+smallurl+'/'
            data = {
                "short_urls": valid_urls,
                "invalid_urls" : [],
                "status": "OK",
                "status_codes": []
            }      
        return JsonResponse(data, status = 200)
    else:
        data = bad_data
    return JsonResponse(data, status = 404)

@csrf_exempt
def longUrls(request):
    data = {}
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        invalid_urls = []
        valid_urls = {}
        short_urls = requestData['short_urls']
        for url in short_urls:
            splitUrl = url.split('/')
            ur = []
            for tt in splitUrl:
                if tt != '' and tt != 'http:' and tt != 'https:':
                    ur.append(tt)
            splitUrl = ur
            utl = splitUrl[1]
            try:
                shortUrl = Shorturl.objects.get(short_url = utl)
                valid_urls[url] = shortUrl.long_url
            except Shorturl.DoesNotExist:
                invalid_urls.append(url)
        if len(invalid_urls) > 0:
            data =  {
                    "invalid_urls" : invalid_urls,
                    "status": "FAILED",
                    "status_codes": ["SHORT_URLS_NOT_FOUND"]
                }
        else:
            data = {
                "long_urls": valid_urls,
                "invalid_urls": [],
                "status": "OK",
                "status_codes": []
            }
        return JsonResponse(data, status = 200)
    else:
        data = bad_data
    return JsonResponse(data, status = 404)