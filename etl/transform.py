import pandas as pd
from extract import extract

def transform():
    # Call the extract function
    df = extract()
    # Transforming dtypes
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce', dayfirst=True)
    # Postal Code sometimes will start from 0
    df['Postal Code'] = df['Postal Code'].astype(str)
    print("Data transformed Successfully!")
    # concat and drop duplicates on Order Date and Ship Date 
    all_dates = pd.concat([df['Order Date'], df['Ship Date']]).drop_duplicates()
    return df, all_dates

# testing function
if __name__ == "__main__":
    df, all_dates = transform()
    print(df.head())
    print(df.dtypes)
    print(all_dates.head())