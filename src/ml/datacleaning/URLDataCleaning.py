from urllib.parse import urlparse

# def http_check(url):
#     url_obj = urlparse(url)
#     if not url_obj.scheme:
#         return False
#     return True

def clean_data(url):
    url_obj = urlparse(url)
    if not url_obj.scheme:
        url = "http://" + url
        return url
    return url