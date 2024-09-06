import pandas as pd

def explore_data(filepath):
    if '.csv' in filepath:
        df = pd.read_csv(filepath)
    elif '.xlsx' in filepath:
        df = pd.read_excel(filepath)

    df = df[["content", "score"]]
    
    # Hard labeled the dataset 
    # (temporary, will be move to new feature later)
    df["label"] = df["score"].map({
        1: 0, # 0: negative
        2: 0, # 0: negative
        3: 1, # 1: neutral
        4: 2, # 2: positive
        5: 2, # 2: positive
    })

    # Only show 200 characters so it will not fill the tables to much
    df['content'] = df['content'].apply(lambda x: x[:200] + '...' if len(x) > 200 else x)

    headers = df.columns.tolist()
    data = df.values.tolist()
    
    return headers, data