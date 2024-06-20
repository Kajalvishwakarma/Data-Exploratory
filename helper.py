from wordcloud import WordCloud
import pandas as pd

def fetch_stats(select_plat, df):
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Kgs/Pieces'] = pd.to_numeric(df['Kgs/Pieces'], errors='coerce')
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]

    # fetch no. companies
    num_comp = df['Platform'].nunique()
    # fetch no. products
    num_uni_product = df['Product'].nunique()
    num_product = df['Kgs/Pieces'].sum()
    total_price = df['Price'].sum()
    # products = []
    # for company in df['Platform']:
    #     products.extend(company.split())

    return num_comp, num_uni_product ,num_product, total_price

# most active companies
def active_companies(df):
    x = df['Platform'].value_counts()
    df = round((df['Platform'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Platform', 'Platform':'Percent'})
    return x, df

#for products
def cloud1(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]

    wc = WordCloud(width=300, height=300, min_font_size=10, background_color='white').generate(
        df['Product'].str.cat(sep=" "))
    return wc

#for platform
def cloud2(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]

    wc1 = WordCloud(width=300, height=300, min_font_size=10, background_color='white').generate(
        df['Platform'].str.cat(sep=" "))
    return wc1

#most sold product
def monthly_earnings(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]
    sales = df.groupby(['Platform', 'Product'])['Kgs/Pieces'].sum().reset_index()
    pivot_data = sales.pivot(index='Platform', columns='Product', values='Kgs/Pieces').fillna(0)
    return pivot_data

#most sold product
def most_earned_company(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]
    sales1 = df.groupby(['Platform','Product'])['Price'].sum().reset_index()
    pivot1 = sales1.pivot(index='Platform', columns='Product', values='Price').fillna(0)
    return pivot1

def pie_most_earned_plat(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]
    sumofcom = df.groupby('Platform')['Price'].sum().reset_index()
    return sumofcom

def pie_most_sold_of_plat(select_plat, df):
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]
    sumofprod = df.groupby('Platform')['Kgs/Pieces'].sum().reset_index()
    return  sumofprod

def monthly_anlysis(select_plat, df): # on the basis of total products
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]

    df['Month_Num'] = df['Buying_Date'].dt.month
    timeline = df.groupby(['Year', 'Month_Num', 'Month']).sum()['Kgs/Pieces'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['Time'] = time
    # timeline.drop('Month', axis = 1)
    return timeline

def monthly_anlysis2(select_plat, df): # on the basis of total prices
    if select_plat != 'Overall':
        df = df[df['Platform'] == select_plat]

    df['Month_Num'] = df['Buying_Date'].dt.month
    timeline1 = df.groupby(['Year', 'Month_Num', 'Month']).sum()['Price'].reset_index()
    time = []
    for i in range(timeline1.shape[0]):
        time.append(timeline1['Month'][i] + "-" + str(timeline1['Year'][i]))
    timeline1['Time'] = time
    # timeline.drop('Month', axis = 1)
    return timeline1