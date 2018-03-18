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
    good_codes = [
        200,
        302
    ]
    if requests.head(url).status_code not in good_codes:
        return False
    return True
    
def hashCode(code=None):
    chars=string.ascii_lowercase + string.digits

    if code == None or code.strip() == '':
        code = ''.join(random.sample(chars*8, 8))
    else:
        try:
            st = Shorturl.objects.get(short_url=code)
        except Shorturl.DoesNotExist:
            return code
        if st:
            return hashCode(code=None)
    return hashCode(code)