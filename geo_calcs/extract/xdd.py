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
    snippets = "https://xdd.wisc.edu/api/snippets"

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
                'fragment_limit': 5,
                'article_limit': 50,
#                'full_results': True,
                'inclusive': True,
                'clean': True,                
                }
            data = request_api(snippets, params, headers)
            temp = get_df_xDD(data)
            temp['location'] = location
            temp['keyword'] = keyword
            df = df.append(temp)

    df = df.drop_duplicates(subset=['_gddid'])
    df = df.set_index('_gddid')
    df = df.sort_values(by='hits', ascending=False)

    return df

def get_term_list(df, col):
    '''
    Given a pandas Dataframe, returns a list.

    Parameters
    ----------
    df : pandas Dataframe
        
    col : string
        The name of t he column to be returned as a list

    Returns
    -------
    term_list : List
    '''
    
    term_list = df[col].tolist()
    term_list = [x for x in term_list if str(x) != 'nan']
    return term_list

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

def distance(s, w1, w2):
    '''
    Measures the proximity between two words.

    Parameters
    ----------
    s : String
        Raw string to parse for distance.
    w1 : String
        First word for comparison.
    w2 : String 
        Second word for comparison.

    Returns
    -------
    Integer
        Number of words between the two comparison words.

    '''
     
    if w1 == w2 :
       return 0
 
    # get individual words in a list
    words = s.split(" ")
    n = len(words)
 
    # assume total length of the string as
    # minimum distance
    min_dist = n+1
 
    # Find the first occurrence of any of the two
    # numbers (w1 or w2) and store the index of
    # this occurrence in prev
    for i in range(n):
         
        if words[i] == w1 or words[i] == w2:
            prev = i
            break
 
    # Traverse after the first occurrence
    while i < n:
        if words[i] == w1 or words[i] == w2:
 
            # If the current element matches with
            # any of the two then check if current
            # element and prev element are different
            # Also check if this value is smaller than
            # minimum distance so far
            if words[prev] != words[i] and (i - prev) < min_dist :
                min_dist = i - prev - 1
                prev = i
            else:
                prev = i
        i += 1       
 
    return min_dist
