# ---- IMPORT LIBRARY ----
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- PLOT SETUP ----
sns.set_theme(style='whitegrid', palette='coolwarm')

# ---- PAGE SETUP ----
st.set_page_config(
    page_title = 'Sales Dashboard',
    page_icon = ':bar_chart:',
    layout='wide'
)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---- LOAD DATA ----
@st.cache
def load_data():
    df = pd.read_csv("D:\Github\sales3.csv")
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.rename(columns={'order_quantity':'qty'}, inplace=True)
    return df
df = load_data()

# ---- PAGE TITLE ----
st.header("Simple Sales Dashboard :bar_chart:")
st.subheader("Created by: **NielKr23**")
st.write('Dataset : https://www.kaggle.com/datasets/dhawyfarrasputra/sales-performance-report-dqlab-store')
st.markdown("---")

# ---- ROW FILTER ----
left, middle, right = st.columns([2,2,8])
with left:
    year_select = st.selectbox(
    'Select Year',
    df.year.sort_values().unique()
)
with middle:
    df2 = df.sort_values('month')
    month_select = st.selectbox(
    'Select Month',
    df2['month_name'].unique()
)

# ---- DATAFRAME SELECTION ----
df_selection = df.query(
    "year == @year_select & month_name == @month_select"
)
df_selection2 = df_selection.iloc[:,[0,2,3,4,5,8]]

# ---- ROW1 ----
left1, left2, left3, middle, right = st.columns([2.5,2.5,2.5,.5,6])       #Sales report and dashboard
with left1:
    st.subheader('Sales Report')
    st.markdown(f'[{month_select}] [{year_select}]')

with left2:
    st.subheader('Yearly Income')
    value = df[df['year'] == year_select]['sales'].sum()
    st.markdown(f'Rp {value:,}.-')

with left3:
    st.subheader(f'Top Sales {year_select}')
    top_ctg = df[df['year'] == year_select].groupby(['product_category']).sum()[['sales']].sort_values('sales', ascending=False).reset_index()
    top_ctg = top_ctg['product_category'][0]
    st.markdown(f'{top_ctg}')


# ---- ROW2 ----
left, middle, right = st.columns([3.9,.1,3])       #dataframe and plot
with left:
    st.dataframe(df_selection2)
    st.caption(f'{df_selection2.shape[0]} rows and {df_selection2.shape[1]} columns')

with right:
    year_sales = df.groupby('year').sum()[['sales']]
    fig = plt.figure(figsize=(10,15))
    plt.subplot(3,1,1)
    sns.lineplot(
        x = year_sales.index,
        y = 'sales',
        data = year_sales
    )
    plt.xticks(df['year'].unique())
    plt.xlabel('Sales Report YoY', fontsize=14)
       
    plt.subplot(3,1,2)
    month_sales = df.groupby(['year','month_name','month']).sum()[['sales']].reset_index().sort_values('month')
    month_sales = month_sales.loc[month_sales['year'] == year_select]
    sns.barplot(
        x='month_name',
        y='sales',
        data=month_sales
    )
    plt.xlabel(f'Sales On {year_select}', fontsize=14)
    plt.show()
    st.pyplot(fig)

# ---- ROW3 ----            #line plot
left, middle, right = st.columns([3,.1,4.9])
with left:
    product_ctg = df[['year','month_name','product_category','sales']]
    product_ctg = product_ctg.groupby(['year','product_category']).sum([['sales']]).reset_index()
    fig = plt.figure()
    sns.barplot(
        x='year',
        y='sales',
        hue='product_category',
        data=product_ctg
    )
    plt.title('Product Category Sales by Year')
    plt.xlabel('')
    plt.ylim((0,3000000000))
    plt.show()
    st.pyplot(fig)

with right:
    dayly_sales = df_selection.groupby('date').sum()[['sales']].reset_index()
    fig = plt.figure(figsize=(10,4))
    sns.lineplot(
        x='date',
        y='sales',
        data=dayly_sales
    )
    plt.xticks([i for i in range(1,32)], [i for i in range(1,32)])
    plt.title((f'Daily sales on [{month_select}] [{year_select}]'))
    plt.grid(False, axis='x')
    plt.xlabel('')
    plt.show()
    st.pyplot(fig)


left, middle, right = st.columns([2,1,4])
with left:
    ctg_sales = df_selection.groupby(['year','product_category']).sum()[['qty']].reset_index()
    fig = plt.figure()
    plt.pie(
        'qty',
        data=ctg_sales,
        autopct='%.0f%%'
    )
    plt.title(f'Qty. Product Sold on [{month_select}] [{year_select}]\nTotal: {ctg_sales.qty.sum()}')
    plt.legend(ctg_sales['product_category'], loc=4)
    plt.show()
    st.pyplot(fig)