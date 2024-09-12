def do_prediction(df, loaded_pickle):
    pred = loaded_pickle.predict(df['content'])

    # change score and pred results into sentiment
    sentiment_mapping = {0: 'negative', 1: 'neutral', 2: 'positive'}
    score_mapping = { # hard-labeled for comparison with pred only
        1: 'negative', 
        2: 'negative', 
        3: 'neutral', 
        4: 'positive', 
        5: 'positive'
    }

    df['pred'] = pred # do prediction
    df['pred'] = df['pred'].map(sentiment_mapping) # map label to sentiment

    headers = ['content', 'score', 'pred']
    data = df[['content', 'score', 'pred']].values.tolist()

    return df, headers, data