# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image


# Setting up page configuration

st.set_page_config(page_title= "Airbnb Data Visualization Dashboard & Analysis",              
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   
                  )

# Creating option menu in the side bar
st.markdown("*Application created by Subbulakshmi*")
selected = option_menu(None, ["Home","Insights","Analysis"], 
                        icons=["house","graph-up-arrow","bar-chart-line"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        orientation="horizontal",
                        styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                "nav-link-selected": {"background-color": "#FF5A5F"}}
                        )


# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
  
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://miro.medium.com/v2/resize:fit:875/0*g2NX1MiZb2fVk6pv.png")
    with col2:
        st.title(':red[Airbnb Data Visualization Dashboard & Analysis]')
        st.write("Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations, typically for short stays.")
        st.write("---")
        st.write(":red[**Technologies Used :**] Python, Pandas, Plotly, Streamlit, MongoDB Atlas")
        st.write(":red[**Overview :**]  To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
        st.markdown(":red[For reference download the cleaned data below]")
        st.download_button("AirbnbData","Airbnb_data.csv")

# OVERVIEW PAGE
if selected == "Insights":

    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                        title='Top 10 Property Types',
                        x='Listings',
                        y='Property_type',
                        orientation='h',
                        color='Property_type',
                        color_continuous_scale=px.colors.sequential.Turbo)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True) 
    
        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df2,
                        title='Top 10 Hosts with Highest number of Listings',
                        x='Listings',
                        y='Host_name',
                        orientation='h',
                        color='Host_name',
                        color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                        title='Total Listings in each Room_types',
                        names='Room_type',
                        values='counts',
                        color_discrete_sequence=px.colors.sequential.Turbo
                    )
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='inside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)
        
        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'],as_index=False)['Listing_Name'].count().rename(columns={'Listing_Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Turbo
                            )
        st.plotly_chart(fig,use_container_width=True)
    
    
        
        
    
# EXPLORE PAGE
if selected == "Analysis":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        
        #HEADING 3
        st.markdown("## Quality Based Review Analysis")
        
        # AVERAGE REVIEW SCORES FOR EACH ROOM TYPE
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="Review_scores")
        avg_review_scores = df.groupby('Room_type')['Review_scores'].mean().reset_index()
        fig = px.pie(avg_review_scores, 
                    values='Review_scores', 
                    names='Room_type',
                    title='Avg Review Scores in each Room Type',
                    color='Room_type',
                    color_discrete_sequence=px.colors.sequential.Plasma)

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale="solar"
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='turbo'
                            )
        st.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("##   ")
        st.markdown("###   ")
        st.markdown("##   ")
        st.markdown("##   ")
        
        
        # AVG REVIEW SCORES BY COUNTRY    
        Avg_review_score = df.pivot_table(index="Country", values="Review_scores", aggfunc="mean").sort_values(by="Review_scores").reset_index()
        fig = px.bar(
            Avg_review_score,
            x='Review_scores',  # X-axis: average review scores
            y='Country',  # Y-axis: countries
            title='Avg Review Scores by Country',
            color='Review_scores',  # Color bars by review scores
            color_continuous_scale='Viridis',  # Color scale
            orientation='h'# Horizontal orientation for better readability
            
           )

        st.plotly_chart(fig, use_container_width=True)
    
        
        
        