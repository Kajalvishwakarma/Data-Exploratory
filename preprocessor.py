import re
import pandas as pd

def preprocess(datas):
    regex = '\d{1,2}/\d{1,2}/\d{2,4},\d{1,2}:\d{2},'
    details = re.split(regex, datas)[1:]
    dates = re.findall(regex, datas)

    df = pd.DataFrame({'Product_Details': details, 'Buying_Date': dates})
    df['Buying_Date'] = pd.to_datetime(df['Buying_Date'], format='%d/%m/%Y,%H:%M,')

    platform = []
    product = []
    measure = []
    price = []
    for details in df['Product_Details']:
        # \w is letters, digits, and underscores
        # \W is anything that's not a word character like spaces, punctuation, etc
        #  + indicates that there can be one or more such characters
        # ? makes the quantifier non-greedy, meaning it matches as few characters as possible
        entry = re.split('([\w\W]+?),([\w\W]+?),([\w\W]+?),([\w\W]+)', details)
        if entry[1:]:
            platform.append(entry[1])
            product.append(entry[2])
            measure.append(entry[3])
            price.append(entry[4])
        else:
            #The string 'no name' is appended to the platform list. This indicates that no platform information was found.
            platform.append('no name')
            product.append(entry[0])
            measure.append(entry[0])# no separate measurement unit
            price.append(entry[0])#no separate price information
    df['Platform'] = platform
    df['Product'] = product
    df['Kgs/Pieces'] = measure
    df['Price'] = price
    df.drop(columns=['Product_Details'], inplace=True)

    df['Year'] = df['Buying_Date'].dt.year
    df['Month_Num'] = df['Buying_Date'].dt.month
    df['Month'] = df['Buying_Date'].dt.month_name()
    df['Day'] = df['Buying_Date'].dt.day
    df['Hour'] = df['Buying_Date'].dt.hour
    df['Minute'] = df['Buying_Date'].dt.minute

    return df

