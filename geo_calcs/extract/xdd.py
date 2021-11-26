"""
API tools. Uses xDD.
"""
import requests
import json
import pandas as pd
import re


def jprint(file):
    """Prints an easier to read json.  I NEED TO TEST THIS.

    Parameters
    ----------
    obj : str
        json file.

    Returns
    -------
    obj
        json object.
    """
    text = json.dumps(file, sort_keys=True, indent=2)
    return text


def request_api(url, params, headers):
    """Requests a response from an API, given the url, paramaters, and
    headers.

    Parameters
    ----------
    url : str
        The url of the API.
    params : dict
        Parameters for the API call.
    headers : dict
        Header information for the API call.

    Returns
    -------
    json
        A json response.

    Raises
    ------
    ValueError
        Could not parse the JSON
    """
    try:
        response = requests.get(url, params=params, headers=headers)
    except ValueError:
        print("Could not parse the JSON.")
    return response.json()


def get_df_xDD(data):
    """Accepts a response from an API call to xDD. Returns a flat and tidy
    pandas dataframe.

    Parameters
    ----------
    data : json
        A json response from API.

    Returns
    -------
    pandas DataFrame
        A flat and tidy dataframe with article metadata.
    """
    df = pd.json_normalize(data)
    df = df['success.data']
    dic = df[0]
    df = pd.DataFrame.from_dict(dic)

    return df


def snippet_search(locations, keywords, headers={}):
    """Uses the xDD snippet search to find highlights from an xDD search,
    combining a list of locations and a list of keywords.

    Parameters
    ----------
    locations : list of str
        A list of the locations to search xDD
    keywords : list of str
        A list of keywords to search xDD.
    headers : dict (Default value = {})
        A dictionary with header information

    Returns
    -------
    pandas DataFrame
        A dataframe of the snippet search results without duplicates and
        sorted by hits.
    """
    snippets = "https://xdd.wisc.edu/api/snippets?"

    locations = locations
    keywords = keywords
    headers = headers
    df = pd.DataFrame(columns=['_gddid', 'pubname', 'publisher', 'title',
                               'doi', 'coverDate', 'URL', 'authors',
                               'highlight', 'hits', 'keywords'])
    for location in locations:
        for keyword in keywords:
            search_term = location + ', '
            search_term = search_term + keyword
            params = {
                'term': search_term,
                'fragment_limit': 500,
                #    'full_results': True,
                'inclusive': True,
                'clean': True,
                }
            data = request_api(snippets, params, headers)
            temp = get_df_xDD(data)
            temp['keywords'] = search_term
            df = df.append(temp)

    df = df.drop_duplicates(subset=['_gddid'])
    df = df.set_index('_gddid')
    df = df.sort_values(by='hits', ascending=False)

    return df


def extract_years(df, column):
    """ Function takes a dataframe and column with imbedded year information
    and inserts a new column 'publication_years', with attempted extraction
    of the year from another named column.
        
    Parameters
    ----------
    df : pandas DataFrame
        dataframe with the source column
    reference : str 
        name of the source column
                   
    Returns
    -------
    pandas DataFrame
           A dataframe with the column publication_year added.
    """
    df['publication_year'] = df[column].apply \
                        (lambda x: re.findall('(\d{4})', x)[0]).astype(int)
    return df


def extract_authors(df, column):
    """ Function takes a dataframe and inserts a new column 'author_list',
    with attempted extraction of the authors from another named column.
    Does not always perform perfectly.
        
    Parameters
    ----------
    df : pandas DataFrame
        dataframe with the source column
    reference : str 
        name of the source column
        
    Returns
    -------
    pandas DataFrame
       A dataframe with the column author_list added.
    """
    df['author_list'] = df[column].apply(lambda x: [word for word,pos in \
                    re.pos_tag(x.replace(',', '').split()) if pos == 'NNP'])
    return df
