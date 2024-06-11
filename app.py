import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
df = pd.read_csv('Data/athlete_events.csv')
df_region = pd.read_csv('Data/noc_regions.csv')

df = preprocessor.preprocess(df,df_region)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://animationvisarts.com/wp-content/uploads/2016/11/Olympics-Logo.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    #medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)



    # overall analysis

if user_menu == 'Overall Analysis':
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Hosts")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Nations")
            st.title(nations)
        with col3:
            st.header("Athletes")
            st.title(athletes)


        nations_over_time = helper.data_over_time(df,'region')
        fig = px.line(nations_over_time, x="Edition", y="region")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)


        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Edition", y="Event")
        st.title("Events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athlete_over_time, x="Edition", y="Name")
        st.title("Athletes over the years")
        st.plotly_chart(fig)

        st.title("No. of Events over time(Every Sport)")
        fig,ax = plt.subplots(figsize=(20,20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                    annot=True)
        st.pyplot(fig)

        st.title("Most successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport = st.selectbox('Select a Sport',sport_list)
        x = helper.most_successful(df,selected_sport)
        st.table(x)



        ## country wise analysis

        
if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)



    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)

    if not pt.empty:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    else:
        st.write("No data available to display the heatmap.")

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)




