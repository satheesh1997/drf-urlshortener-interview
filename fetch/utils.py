from .models import Shorturl
import requests, string, random


def validateUrl(url):
    if url is None or url.strip() == "":
        return False
    splitUrl = url.split('/')
    ur = []
    for tt in splitUrl:
        if tt != '' and tt != 'http:' and tt != 'https:':
            ur.append(tt)
    splitUrl = ur
    if len(splitUrl) < 2:
        return False
    try:
        request = requests.get(url)
        if request.status_code != 200:
            return False
    except:
        return False
    return True

def hashCode(code=None):
    chars=string.ascii_lowercase + string.digits

    if code == None or code.strip() == '':
        code = ''.join(random.sample(chars*8, 8))
    else:
        try:
            st = Shorturl.objects.get(short_url=code)
            return hashCode(code=None)
        except Shorturl.DoesNotExist:
            return code
    return hashCode(code)