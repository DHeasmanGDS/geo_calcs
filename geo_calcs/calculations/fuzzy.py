"""
Fuzzy Match Strings and process data for matching and finding duplicates.
Various functions to process data also included.
"""
import numpy as np
from fuzzywuzzy import fuzz


def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ Function computes the minimum edit distance between to strings using
    Levenshteins algorithm. Implements dynamic programming. Can give a ratio
    calculation or print a string showing the number of edits needed.
        
    Parameters
    ----------
    s : str
        first string
    t : str 
        second string
    ratio_calc : bool (Default value = False)
        if true, returns a ratio instead of the number of edits.

    Returns
    -------
    int
        An integer showing number of edits
    float 
        A ratio (length of both strings - number of edits) / length 
        of both strings
    """
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows,cols),dtype=int)  


    for i in range(1, rows):
        for k in range(1,cols):                  
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1,cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,
                                     distance[row][col-1] + 1,
                                     distance[row-1][col-1] + cost)
    if ratio_calc == True:
        ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return ratio
    else:
        print(distance)
        return distance[row][col]
    

def similar_ref(a1, a2, sensitivity=85):
    """ Function returns the partial ratio of two strings if it exceeds a
    given sensitivity.
        
    Parameters
    ----------
    a1 : str
        first string.
    a2 : str 
        second string.
    sensitivity : int (Default value = 85)
        integer from 0 to 100 to determine cutoff
        
    Returns
    -------
    float
        The partial ratio or 0.
    """
    p_ratio = fuzz.partial_ratio(a1, a2)
    if p_ratio > sensitivity:
        return p_ratio
    else:
        return 0    

def find_max_partial_ratio(df, column, sensitivity=85):
    """ Function takes a dataframe and inserts two new columns
    'partial_ratio_max' and 'max_duplicate_index'. The first column compares
    each entry from a df column with each other, and tracks the partial_ratio
    values. The max is then added to the list, and the index of this max is
    added to the second column.
        
    Parameters
    ----------
    df : pandas DataFrame 
        dataframe with the source column
    column : str 
        name of the source column
    sensitivity : int (Default value = 85) 
        integer from 0 to 100 to determine cutoff
                   
    Returns
    -------
    pandas DataFrame
           A dataframe with the columns partial_ratio_max and
           max_duplicate_index added.
    """
    list_to_match = df[column]
    list_of_max = []                            
    list_of_max_indexed = []
    for i in list_to_match:
        max_list = []
        for column in df[[column]]:
            columnSeriesObj = df[column]
            for ref in columnSeriesObj:
                if (i == ref) == False:    
                    max_list.append(similar_ref(i,ref,sensitivity))
        list_of_max.append(max(max_list))
        list_of_max_indexed.append(np.argmax(max_list))
    df['partial_ratio_max'] = list_of_max
    df['max_duplicate_index'] = list_of_max_indexed
    
    return df


