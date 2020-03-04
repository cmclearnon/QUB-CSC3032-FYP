import whois
import re

def extract(url):
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

