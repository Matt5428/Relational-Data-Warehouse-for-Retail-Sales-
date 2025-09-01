import pandas as pd

# extract the data from a .csv file 
def extract():
    try:
        df = pd.read_csv('./data/Global_Superstore2.csv')
        print(f"Data extracted successfully. with {df.shape[0]} rows and {df.shape[1]} colunms")
        return df
# handle missing file error
    except FileNotFoundError as e:
        print(f"Failed to extract: {e.filename} not found.")
        return None

# for testing the function running correctly and check the data types
if __name__ =='__main__':
    df = extract()
    print(df.head())
    print(df.dtypes)