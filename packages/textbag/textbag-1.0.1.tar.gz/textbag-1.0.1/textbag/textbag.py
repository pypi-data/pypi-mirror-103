import nltk
import string
import pandas as pd
import numpy as np


def _clean_string(text):
    '''Remove punctuation and stopwords, and put into lower case.

    Args:
        text (str): text to be cleaned--text will have stopwords and
            punctuation removed, and will be put into lower case.

    Returns:
        cleaned_text (str): Text cleaned. Can be an empty string.
    '''
    
    # Stop words and punctuations to remove.
    stopwords = nltk.corpus.stopwords.words('english')
    punctuation = string.punctuation
    
    tokenized_text = nltk.word_tokenize(text)
    
    # Remove stop words and punctuation.
    text_clean = [word for word in tokenized_text if word not in stopwords]
    text_clean = [word for word in text_clean if word not in punctuation]

    # Merge remaining tokens back into a string.
    cleaned_text = ' '.join(text_clean).lower()

    return cleaned_text


def _clean_numpy(text_array):
    '''Apply _clean_string to text entries in a numpy array.

    Args:
        text_array (numpy array): numpy array with string entries. The shape of
            the array should be (length,) or (length, 1).

    Returns:
        cleaned_text_array (numpy array): cleaned version of text_array.
    '''

    arr_shape = text_array.shape # Remember original dimensions.
    cleaned_text_array = text_array.copy().reshape((-1,)) # Flatten a copy.

    print('Cleaning text')

    for i in range(len(cleaned_text_array)):
        cleaned_text_array[i] = _clean_string(cleaned_text_array[i])

        # Print progress.
        percent_done = (i / len(cleaned_text_array))*100
        print('%.3f%% done' % percent_done, end='\r')
    
    cleaned_text_array = cleaned_text_array.reshape(arr_shape)

    return cleaned_text_array


def _clean_pandas(text_series):
    '''Apply _clean_string to string entries in a pandas series/dataframe.

    Args:
        text_series (pandas series or pandas dataframe):
            Pandas series/dataframe with string entries. If it is a dataframe,
            the shape should be (length, 1).

    Returns:
        (pandas series or pandas dataframe): A cleaned series if text_series 
            was a series object, a cleaned dataframe if text_series was a 
            dataframe object.
    '''

    if type(text_series) is pd.core.series.Series:
        text_array = text_series.to_numpy()
        cleaned_text_array = _clean_numpy(text_array)

        return pd.Series(cleaned_text_array)

    elif type(text_series) is pd.core.frame.DataFrame:
        text_array = text_series.to_numpy()
        cleaned_text_array = _clean_numpy(text_array)

        return pd.DataFrame(cleaned_text_array)


def important_text(text_data):
    '''Remove unimportant words and punctuation from text data.

    Args:
        text_data (str, numpy array, pandas series, or pandas dataframe):
            Text data to be cleaned. If numpy array then should be (length,) 
            or (length, 1). If pandas dataframe then the shape should be 
            (length, 1).

    Returns:
        (str, numpy array, pandas series, or pandas dataframe):
            Cleaned text data of the same type passed.
    '''

    if type(text_data) is str:
        return _clean_string(text_data)

    elif type(text_data) is np.ndarray:
        return _clean_numpy(text_data)

    elif isinstance(text_data, (pd.core.frame.DataFrame, pd.core.series.Series)):
        return _clean_pandas(text_data)


def _string_lexicon(text):
    '''Create a set with words from a string as elements.

    Args:
        text (str)

    Returns:
        bag (set): A set of which the elements are the words from the text passed.
    '''

    lex = set(nltk.word_tokenize(text))
    
    return lex


def _numpy_lexicon(text_array):
    '''Use _string_bagger on text entries in a numpy array.

    Args:
        text_array (numpy array): numpy array with string entries. The shape of
            the array should be (length,) or (length, 1).

    Returns:
        bag (set): A set of which the elements are the words from the text passed.
    '''

    text_array_copy = text_array.copy().reshape((-1,))
    
    print('Creating lexicon')

    lex = set()
    for i in range(len(text_array_copy)):
        lex = lex.union(_string_lexicon(text_array_copy[i]))

        # Print progress.
        percent_done = (i / len(text_array_copy))*100
        print('%.3f%% done' % percent_done, end='\r')

    return lex


def _pandas_lexicon(text_series):
    '''Use _string_lexicon on text entries in a pandas series/dataframe.

    Args:
        text_series (pandas series or pandas dataframe): 
            Pandas series/dataframe with string entries. If it is a dataframe,
            the shape should be (length,) or (length, 1).

    Returns:
        bag (set): A set of which the elements are the words from the text passed.
    '''

    lex = _numpy_lexicon(text_series.to_numpy())

    return lex


def lexicon(text_data):
    '''Create a lexicon, given text data.

    Args:
        text_data (str, numpy array, pandas series, or pandas dataframe):
            Text data to be cleaned. If numpy array then should be (length,) 
            or (length, 1). If pandas dataframe then the shape should be 
            (length, 1).

    Returns:
        (set): A set of which the elements are the words from the text passed.
    '''

    if type(text_data) is str:
        return _string_lexicon(text_data)

    elif type(text_data) is np.ndarray:
        return _numpy_lexicon(text_data)

    elif isinstance(text_data, (pd.core.frame.DataFrame, pd.core.series.Series)):
        return _pandas_lexicon(text_data)


def _string_bagger(text, lex): 
    '''Create bag-of-words representation for a string.

    Args: 
        text (str): A string.
  
        lex (set): Set containing all words to be considered in bag-of-words 
            representation. Can contain more words than text_data.

    Returns:
        bag (dict) Bag-of-words representation of text data passed, with respect
            to lex.
    '''

    bag = dict.fromkeys(lex, []) # Empty bag.
    word_freq = dict.fromkeys(lex, 0) # Word frequency counter dictionary.

    tokens = nltk.word_tokenize(text) 

    # Count words in passed text.
    for word in tokens:
        word_freq[word] += 1
    
    for word in bag:
        bag[word] = bag[word][:] # Shallow copy prevents updating all lists.
        bag[word].append(word_freq[word])

    return bag


def _numpy_bagger(text_array, lex): 
    '''Create bag-of-words representation for a numpy array of text data.

    Args:
        text_array (numpy array): numpy array with string entries. The shape of
            the array should be (length,) or (length, 1).

        lex (set): Set containing all words to be considered in bag-of-words 
            representation. Can contain more words than text_data.

    Returns:
        bag (dict) Bag-of-words representation of text data passed, with respect
            to lex.
    '''

    text_array_copy = text_array.copy().reshape((-1,))

    bag = dict.fromkeys(lex, [])

    print(f'Bagging {len(text_array_copy)} items')

    for i in range(len(text_array_copy)):
        word_freq = dict.fromkeys(lex, 0)
        tokens = nltk.word_tokenize(text_array_copy[i]) 

        for word in tokens:
            word_freq[word] += 1
        
        for word in bag:
            bag[word] = bag[word][:]
            bag[word].append(word_freq[word])

        # Print progress.
        percent_done = (i / len(text_array_copy))*100
        print('%.3f%% done' % percent_done, end='\r')

    return bag


def _pandas_bagger(text_series, lex):
    '''Create bag-of-words representation for a pandas series/dataframe of text data.

    Args:
        text_series (pandas series or pandas dataframe): 
            Pandas series/dataframe with string entries. If it is a dataframe,
            the shape should be (length,) or (length, 1).

        lex (set): Set containing all words to be considered in bag-of-words 
            representation. Can contain more words than text_data.

    Returns:
        bag (dict) Bag-of-words representation of text data passed, with respect
            to lex.
    '''

    bag = _numpy_bagger(text_series.to_numpy(), lex)
    
    return bag


def text_bag(text_data, lex):
    '''Create a bag-of-words representation, given text data.

    Args:
        text_data (str, numpy array, pandas series, or pandas dataframe):
            Text data to be cleaned. If numpy array then should be (length,) 
            or (length, 1). If pandas dataframe then the shape should be 
            (length, 1).

        lex (set): Set containing all words to be considered in bag-of-words 
            representation. Can contain more words than text_data.

    Returns:
        (dict) Bag-of-words representation of text data passed, with respect
            to lex.
    '''

    if type(text_data) is str:
        return _string_bagger(text_data, lex)

    elif type(text_data) is np.ndarray:
        return _numpy_bagger(text_data, lex)

    elif isinstance(text_data, (pd.core.frame.DataFrame, pd.core.series.Series)):
        return _pandas_bagger(text_data, lex)
