"""
Tools to extract data from the web
"""
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

def bulk_zip_download(base_url, sub_links):
    """Downloads bulk .zip files from a base url with multiple subdirectories.
    The downloads go into an output subdirectory created at the root 
    directory.
    
    Parameters
    ----------
    base_url : str
        The base url 
    sub_links : list of str
        A list of strings of the subdirectories to search through
    
    Returns
    -------
    None
    """
    for sub_link in sub_links:
        sub_url = base_url + sub_link
        r  = requests.get(sub_url)
        data = r.text
        soup = BeautifulSoup(data)
        link_list = []
        filtered_link_list = []

        for link in soup.find_all('a'):
            link_list.append(link.get('href'))

        regex = re.compile(r'^.*\.(zip|ZIP)$')
        filtered_link_list = [i for i in link_list if regex.search(i)]
        
        for l in filtered_link_list:
            file_url = sub_url + l
            r = requests.get(file_url)
            Path('output/' + sub_link + '/').mkdir(parents=True, exist_ok=True)
            open(str('output/' + sub_link + '/' +l), 'wb').write(r.content)
