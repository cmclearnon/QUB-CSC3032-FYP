import urllib.parse
import whois
import re
from tld import get_tld, is_tld
from urllib.parse import urlparse
import pandas as pd
import numpy as np
import datetime
from socket import *

def clean_data(url):
    url_obj = urlparse(url)
    if not url_obj.scheme:
        url = "http://" + url
        return url
    return url

"""
    Extract lexical based features from the URL strings in the dataset. These features include:
    - Length of URL
    - Length of Hostname
    - Path length
    - TLD Length
    - Special Char Count
    - '.-@%=?' Char Count
    - Digit Count
    - Unique Char Count
"""

def lexical_extract(url):
    if not url:
        return

    url_dt = {}

    url_len = len(url)
    url_dt.update({"URLLength": url_len})

    url_rg = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_rg, url)
    host_len = len(url_search.group('host'))
    url_dt.update({"HostLength": host_len})

    parsed_tld = get_tld(url, fix_protocol=True, fail_silently=True)
    if parsed_tld is None:
        url_dt.update({"TLDLength": 0})
    else:
        tld_len = len(parsed_tld)
        url_dt.update({"TLDLength": tld_len})

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


    d_count = sum(list(map(lambda x:1 if x.isdigit() else 0, list(url))))
    url_dt.update({"DigitCount": d_count})

    un_ch_count = len(set(url))
    url_dt.update({"UniqueCharCount": un_ch_count})

    return url_dt


"""
    This function extracts any domain specific features from the URL to add to the dataset model
"""
def host_extract(url):
    if not url:
        return
    
    feature_list = []
    url_dt = {}
    url_regex = '(?:http.*://)?(?P<host>[^:/ ]+).*'
    url_search = re.search(url_regex, url)
    hostname = url_search.group('host')

    try:
        domain = whois.whois(hostname)
    except (whois.parser.PywhoisError, timeout, gaierror, ConnectionResetError, ConnectionRefusedError):
        url_dt.update({
            "RegistryDate": pd.NaT,
            "ExpirationDate": pd.NaT,
            "HostCountry": None,
            "DomainAge": np.NaN
        })
        
        feature_list.append(url_dt)
        df = pd.DataFrame(feature_list)
        return df
        
    reg_date = domain.creation_date
    if isinstance(reg_date, list):
        url_dt.update({"RegistryDate": reg_date[0]})
    elif (reg_date is None) or (reg_date == ""):
        url_dt.update({"RegistryDate": pd.NaT})
    else:
        try:
            url_dt.update({"RegistryDate": pd.to_datetime(reg_date)})
        except ValueError:
            url_dt.update({"RegistryDate": pd.NaT})

    exp_date = domain.expiration_date
    if isinstance(exp_date, list):
        url_dt.update({"ExpirationDate": exp_date[0]})
    elif (exp_date is None) or (exp_date == ""):
        url_dt.update({"ExpirationDate": pd.NaT})
    else:
        try:
            url_dt.update({"ExpirationDate": pd.to_datetime(exp_date)})
        except ValueError:
            url_dt.update({"ExpirationDate": pd.NaT})

    country = domain.country
    url_dt.update({"HostCountry": country})

    if pd.isnull(url_dt["RegistryDate"]):
        domain_age = np.NaN
        url_dt.update({"DomainAge": domain_age})
    else:
        domain_age = datetime.datetime.now() - url_dt["RegistryDate"]
        age_in_days = domain_age.days
        url_dt.update({"DomainAge": age_in_days})

    feature_list.append(url_dt)
    df = pd.DataFrame(feature_list)
    
    return df
