import urllib.parse
import re
from tld import get_tld

def extract_lexical_features(url):
    url_dt = []
    """
    This function extracts all Lexical based features of the URL string
    """

    # TODO: Length of URL
    url_len = len(url)
    url_dt.append(url_len)

    # TODO: Length of Hostname
    url_rg = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_rg, url)
    host_len = len(url_search.group('host'))
    url_dt.append(host_len)
    #host_len = len(urlparse(url).hostname)

    # TODO: Length of Path

    # TODO: Length of Top Level Domain
    tld_len = len(get_tld(url))
    url_dt.append(tld_len)

    # TODO: Count of special characters

    # TODO: Count of '.'
    dot_count = str(url).count('.')
    url_dt.append(dot_count)

    # TODO: Count of '-'
    dash_count = str(url).count('-')
    url_dt.append(dash_count)

    # TODO: Count of '@'
    at_count = str(url).count('@')
    url_dt.append(at_count)

    # TODO: Count of '%'
    percent_count = str(url).count('%')
    url_dt.append(percent_count)

    # TODO: Count of '='
    equals_count = str(url).count('=')
    url_dt.append(equals_count)

    # TODO: Count of '?'
    question_mark_count = str(url).count('?')
    url_dt.append(question_mark_count)

    # TODO: Is executable

    # TODO: Count of digits
    d_count = sum(list(map(lambda x:1 if x.isdigit() else 0, list(url))))
    url_dt.append(d_count)

    # TODO: Count of unique characters
    un_ch_count = len(set(url))
    url_dt.append(un_ch_count)

    # TODO: Is IP address
    return url_dt

