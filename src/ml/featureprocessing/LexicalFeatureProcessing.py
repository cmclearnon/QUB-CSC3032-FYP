import urllib.parse
import re
from tld import get_tld, is_tld

def extract(url):
    #url_dt = []
    url_dt = {}
    """
    This function extracts all Lexical based features of the URL string
    """

    # TODO: Length of URL
    url_len = len(url)
    #url_dt.append(url_len)
    url_dt.update({"URLLength": url_len})

    # TODO: Length of Hostname
    url_rg = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_rg, url)
    host_len = len(url_search.group('host'))
    #url_dt.append(host_len)
    url_dt.update({"HostLength": host_len})
    #host_len = len(urlparse(url).hostname)

    # TODO: Length of Path

    # TODO: Length of Top Level Domain
    parsed_tld = get_tld(url, fix_protocol=True, fail_silently=True)
    if parsed_tld is None:
        url_dt.update({"TLDLength": 0})
    else:
        tld_len = len(parsed_tld)
        url_dt.update({"TLDLength": tld_len})
    # elif not is_tld(url):
    #     url_dt.update({"TLDLength": 0})

    # TODO: Count of special characters

    # TODO: Count of '.'
    dot_count = str(url).count('.')
    #url_dt.append(dot_count)
    url_dt.update({"DotCount": dot_count})

    # TODO: Count of '-'
    dash_count = str(url).count('-')
    #url_dt.append(dash_count)
    url_dt.update({"DashCount": dash_count})

    # TODO: Count of '@'
    at_count = str(url).count('@')
    #url_dt.append(at_count)
    url_dt.update({"@Count": at_count})

    # TODO: Count of '%'
    percent_count = str(url).count('%')
    #url_dt.append(percent_count)
    url_dt.update({"%Count": percent_count})

    # TODO: Count of '='
    equals_count = str(url).count('=')
    #url_dt.append(equals_count)
    url_dt.update({"=Count": equals_count})

    # TODO: Count of '?'
    question_mark_count = str(url).count('?')
    #url_dt.append(question_mark_count)
    url_dt.update({"?Count": question_mark_count})

    # TODO: Is executable

    # TODO: Count of digits
    d_count = sum(list(map(lambda x:1 if x.isdigit() else 0, list(url))))
    #url_dt.append(d_count)
    url_dt.update({"DigitCount": d_count})

    # TODO: Count of unique characters
    un_ch_count = len(set(url))
    #url_dt.append(un_ch_count)
    url_dt.update({"UniqueCharCount": un_ch_count})

    # TODO: Is IP address
    return url_dt

