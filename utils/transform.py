import pandas as pd
import numpy as np

def transform_data(data: list) -> pd.DataFrame:

    try:
        df = pd.DataFrame(data)

        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        df = df[df['Title'] != 'Unknown Product'].copy()
        df = df[df['Price'] != 'Price Unavailable']
        df = df[df['Rating'] != 'Not Rated']

        df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
        df['Price'] = df['Price'] * 16000

        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)

        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(float)

        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False)

        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False)

        df.dropna(inplace=True)

        df = df.astype({
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Title': 'object',
            'Size': 'object',
            'Gender': 'object',
            'timestamp': 'object' 
        })
        
        print("Transformasi data berhasil.")
        return df

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame() 