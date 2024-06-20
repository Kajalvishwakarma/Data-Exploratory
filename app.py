import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt

st.sidebar.title("Sales Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    datas = bytes_data.decode("utf-8")
    #st.text(datas)
    df = preprocessor.preprocess(datas)
    st.title("Given Dataset: ")
    st.dataframe(df)

    # # fetch unique companies
    company = df['Platform'].unique().tolist()
    #company.remove('group_notification')
    company.sort()
    company.insert(0, "Overall")

    select_plat = st.sidebar.selectbox("Show analysis wrt", company)
    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_comp, num_uni_product, num_product, total_price = helper.fetch_stats(select_plat, df)  # recieve
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Companies")
            st.title(num_comp)
        with col2:
            st.header("Unique Products")
            st.title(num_uni_product)
        with col3:
            st.header("Total Products")
            st.title(num_product)
        with col4:
            st.header("Total Earnings")
            st.title(total_price)

    if select_plat == 'Overall':
        st.title("Top Company")
        x, new_df = helper.active_companies(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            ax.barh(x.index, x.values)
            plt.xlabel("Highest Rank")
            plt.ylabel("Platforms")
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

# wordcloud for platforms
    st.title("Most Sold Products")
    wc = helper.cloud1(select_plat, df)
    fig, ax = plt.subplots()
    # plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
    st.pyplot(fig)

    # wordcloud for products
    st.title("Most Appeared Platforms")
    wc1 = helper.cloud2(select_plat, df)
    fig, ax = plt.subplots()
    # plt.figure()
    plt.imshow(wc1, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
    st.pyplot(fig)

    #most products sold by each company Earning
    st.title('Most Sold Products')
    pivot_data = helper.monthly_earnings(select_plat, df)
    fig, ax = plt.subplots()
    pivot_data.plot(kind='line', marker='*', ax = ax)
    plt.xlabel('Company')
    plt.ylabel('Quantity')
    plt.xticks(rotation=45)
    plt.legend(title='Product')
    plt.tight_layout()
    st.pyplot(fig)

    #each company Earning
    st.title('Most Earned Products')
    pivot1 = helper.most_earned_company(select_plat, df)
    fig, ax = plt.subplots()
    pivot1.plot(kind='line', marker='o', ax = ax)
    #plt.title('Most Earned Products')
    plt.xlabel('Company')
    plt.ylabel('Earnings')
    plt.xticks(rotation=45)
    plt.legend(title='Product')
    plt.tight_layout()
    st.pyplot(fig)

    #most earned company piechart
    sumofcom = helper.pie_most_earned_plat(select_plat, df)
    st.title("Pie Chart For Most Earned Platform")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(sumofcom)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(sumofcom['Price'], labels=sumofcom['Platform'], radius=3.5,
                colors=['indigo', 'pink', 'lightgreen', 'skyblue', 'orange', 'green', 'blue', 'white', 'brown', 'green',
                        'purple', 'black'])
        #plt.show()
        st.pyplot(fig)

    #most products sold of platform - piechart
    sumofprod = helper.pie_most_sold_of_plat(select_plat, df)
    st.title("Pie chart For Most Sold Product Of Platform")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(sumofprod)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(sumofprod['Kgs/Pieces'], labels = sumofprod['Platform'], radius = 3.5,
               colors=['indigo', 'pink', 'lightgreen', 'skyblue', 'orange', 'green', 'blue', 'white', 'brown','green','purple','black'])
        st.pyplot(fig)

    #Monthly analysis for products
    timeline = helper.monthly_anlysis(select_plat, df)
    st.title("Monthly Analysis On The Basis Of Total Products Sold")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(timeline)
    with col2:
        fig, ax = plt.subplots()
        ax.plot(timeline['Month'], timeline['Kgs/Pieces'])
        plt.xticks(rotation='vertical')
        plt.xlabel("Months")
        plt.ylabel("Quantity")
        st.pyplot(fig)

#Monthly analysis for prices
    timeline1 = helper.monthly_anlysis2(select_plat, df)
    st.title("Monthly Analysis On The Basis Of Total Earnings")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(timeline1)
    with col2:
        fig, ax = plt.subplots()
        ax.plot(timeline['Month'], timeline1['Price'])
        plt.xticks(rotation='vertical')
        plt.xlabel("Months")
        plt.ylabel("Earnings")
        st.pyplot(fig)
