import urllib.parse
import whois
import re
from tld import get_tld, is_tld

def clean_data(url):
    url_obj = urlparse(url)
    if not url_obj.scheme:
        url = "http://" + url
        return url
    return url

def lexical_extract(url):
    """
    Extract lexical based features from the URL strings in the dataset. These features include:
    - Length of URL
    - Length of Hostname
    - Path length
    - TLD Length
    - Special Char Count
    - '.-@%=?' Char Count
    - Digit Count
    - Unique Char Count"""

    if not url:
        return

    url_dt = {}

    url_len = len(url)
    url_dt.update({"URLLength": url_len})

    url_rg = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_rg, url)
    host_len = len(url_search.group('host'))
    url_dt.update({"HostLength": host_len})

    # TODO: Length of Path

    parsed_tld = get_tld(url, fix_protocol=True, fail_silently=True)
    if parsed_tld is None:
        url_dt.update({"TLDLength": 0})
    else:
        tld_len = len(parsed_tld)
        url_dt.update({"TLDLength": tld_len})

    # TODO: Count of special characters

    dot_count = str(url).count('.')
    url_dt.update({"DotCount": dot_count})

    dash_count = str(url).count('-')
    url_dt.update({"DashCount": dash_count})

    at_count = str(url).count('@')
    url_dt.update({"@Count": at_count})

    percent_count = str(url).count('%')
    url_dt.update({"%Count": percent_count})

    equals_count = str(url).count('=')
    url_dt.update({"=Count": equals_count})

    question_mark_count = str(url).count('?')
    url_dt.update({"?Count": question_mark_count})

    # TODO: Is executable


    d_count = sum(list(map(lambda x:1 if x.isdigit() else 0, list(url))))
    url_dt.update({"DigitCount": d_count})

    un_ch_count = len(set(url))
    url_dt.update({"UniqueCharCount": un_ch_count})

    # TODO: Is IP address


    return url_dt


def host_extract(url):
    """
    This function extracts any domain specific features from the URL to add to the dataset model
    """

    # Registry date of Domain
    url_regex = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_regex, url)
    hostname = url_search.group('host')

    domain = whois.query(hostname)
    reg_date = domain.creation_date
    print(reg_date)

    # TODO: PageRank

    # TODO: Google Index

    # TODO: Is in Alexa Top 1 Million Websites

