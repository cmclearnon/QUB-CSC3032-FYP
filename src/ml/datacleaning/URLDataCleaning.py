from urllib.parse import urlparse

def http_check(url):
    url_obj = urlparse(url)
    if not url_obj.scheme:
        return False
    return True

def clean_data(url):
    if http_check(url) == False:
        url = "http://" + url
    return url