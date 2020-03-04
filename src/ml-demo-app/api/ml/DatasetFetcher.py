import requests
import logging
import json
import os
import zipfile
import io

from shutil import copyfile
from urllib.parse import urlparse

class DatasetFetcher():
    def __init__(self, source, file_path):
        self.source = source
        self.file_path = file_path

    def fetch_file_local():
        if check_if_csv(file_path=self.file_path):
            new_file_path = os.getcwd()+'/data/tmp'
            copyfile(self.file_path, new_file_path)
            # return new_file_path
        return 'Chosen file is not a CSV file type.'

    def fetch_file_url(self, url, filename):
        u = urlparse(url)
        print(url)
        if u is None:
            return 'URL is malformed or is an invalid URL.'
        if self.is_downloadable_file(url) is False:
            return 'URL does not reference a downloadable file.'
        if self.check_if_csv(file_path=url):
            r = requests.get(url, allow_redirects=True)
            new_file_path = os.getcwd()+'/data/tmp'
            open(new_file_path+f'/{filename}.csv', 'wb').write(r.content)

    @staticmethod
    def check_if_csv(file_path: str):
        if file_path.lower().endswith(('.csv')):
            return True
        return False

    def is_downloadable_file(self, url):
        h = requests.head(url, allow_redirects=True)
        print(f'Headers: {h.headers}')
        headers = h.headers
        content_type = headers.get('content-type')
        print(content_type)

        if 'html' in content_type.lower():
            return content_type
        if 'text' in content_type.lower():
            return content_type
        
        return True

        