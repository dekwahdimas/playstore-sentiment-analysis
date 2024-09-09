import re

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def nltk_pre_processing(content):
    # Tokenize content
    tokens = word_tokenize(content)

    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text

def do_pre_processing(filepath):
    if '.csv' in filepath:
        df = pd.read_csv(filepath)
    elif '.xlsx' in filepath:
        df = pd.read_excel(filepath)

    # Clean the content/review
    df['content'] = df['content'].apply(lambda x: x.lower())
    df['content'] = df['content'].apply(lambda x: re.sub(r'[\W_?|$|.!_:"(-+,@#]', ' ', x))
    df['content'] = df['content'].apply(lambda x: re.sub(r'\d+', ' ', x))
    df['content'] = df['content'].apply(lambda x: re.sub(r'\b[a-zA-Z]\b', ' ', x))
    df['content'] = df['content'].apply(lambda x: re.sub(r'\s+', ' ', x))
    df['content'] = df['content'].apply(lambda x: re.sub(r'\n', ' ', x))

    # Use NLTK
    df['content'] = df['content'].apply(nltk_pre_processing)

    # Drop null data after being processed
    df = df.dropna()
    
    headers = df.columns.tolist()
    data = df.values.tolist()

    return df, headers, data
