#Import packages
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import leafmap.foliumap as leafmap
from statsmodels.formula.api import ols

#Style
st.set_page_config(
    page_title="Eindpresentatie VA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state = 'collapsed',
)

#Title
st.markdown("<h1 style='text-align: center; color: grey;'>🌎Dashboard WHO gevolg van overlijden🌎</h1>", unsafe_allow_html=True)

#Create header

st.markdown("<h4 style='text-align: center; color: grey;'>Visual Analytics eindopdracht gemaakt door: Maureen Dewki & Dinand Kruger</h4>", unsafe_allow_html=True)

#Import datasets
wereld = pd.read_csv('wereld.csv', index_col=[0])
alles = pd.read_csv('alles.csv', index_col=[0])
india =pd.read_csv('india.csv', index_col=[0])


# Nav bar 
selected = option_menu(
    menu_title=None,  
    options=["Wereld","Landen vergelijken", "Kaart", "Model"],  
    icons=["globe", "bar-chart","map", "bezier"],   
    default_index=0,  
    orientation="horizontal",
)

#Page one
if selected == "Wereld":
    components.html(
    """
        <div style="text-align: center">
            <a href="https://www.kaggle.com/datasets/varpit94/worldwide-deaths-by-risk-factors/download?datasetVersionNumber=1" target="_blank" class="button">Link naar WHO data🔗</a>
            
            </div>
    """
    """
        <div style="text-align: center">
            
            <a href="https://www.kaggle.com/datasets/vaishnavivenkatesan/world-population/download?datasetVersionNumber=1" target="_blank" class="button">Link naar wereldpopulatie data🔗</a>
            </div>
    """
    """
        <div style="text-align: center">
            
            <a href="https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv" target="_blank" class="button">Link naar coördinaten van landen🔗</a>
            </div>
    """
    , height= 72)

    #sidebar
    _id = st.sidebar.slider('Aantal landen geselecteerd', 1 , 231, 10)

    #vis 1
    df_plot = alles[['Country Name', 'Total Deaths']].groupby('Country Name')
    df_plot = df_plot.agg('sum').sort_values(by = 'Total Deaths', ascending = False).head(_id)
    df_plot.reset_index(inplace = True)
    fig = px.histogram(df_plot, x= 'Country Name', y='Total Deaths')
    fig.update_layout(height = 900, title = 'Top 10 landen met meeste overledenen')
    st.plotly_chart(fig,use_container_width=True)
    
    #vis 2
    grouped_country_df = wereld.groupby('Country Name').mean()
    total_deaths = grouped_country_df.drop('Year', axis=1).sum().transpose().sort_values(ascending=False)
    total_deaths =  total_deaths.drop('Total Deaths')
    fig = plt.figure(figsize=(20,7), dpi=50)
    sns.barplot(y=total_deaths.index, x=total_deaths.values).set(title='Doodsoorzaken in de wereld')
    plt.xlabel('Aantal doden in miljoenen')
    st.write(fig)

    #vis 3
    box = wereld[['High systolic blood pressure', 'Smoking', 'High fasting plasma glucose', 'Country Name', 'Year']]
    box = box[wereld['Country Name']=='World']
    fig = go.Figure()
    fig.add_trace(go.Box(y=box.Smoking, name='Smoking', marker_color = 'indianred'))
    fig.add_trace(go.Box(y=box['High systolic blood pressure'], name= 'High systolic blood ', marker_color='blue'))
    fig.add_trace(go.Box(y=box['High fasting plasma glucose'], name = 'High fasting plasma glucose', marker_color = 'lightseagreen'))
    fig.update_layout(title = 'Top 3 Doodsoorzaken In De Wereld', yaxis_title='Aantal doden', height = 900)
    st.plotly_chart(fig,use_container_width=True)

#Page two
if selected == "Landen vergelijken":  
    col1, col2  = st.columns(2)
    #left side  
    with col1: 
        options_left = st.selectbox('Selecteer het eerste land',alles['Country Name'].unique(), index=114)
        selected_data_left = alles[alles['Country Name']==options_left]
        risk_factors = [rf for rf in selected_data_left.columns if rf not in ['Country Name','Year', 'latitude', 'longitude','verhouding','Total Deaths', 'Inhabitants', 'Country Code' ]]
        average_deaths = []
        for rf in risk_factors:
            average_deaths.append(selected_data_left[rf].mean())
        df_left = pd.DataFrame(list(zip(risk_factors,average_deaths)),columns=['Risk Factor','Avg. Deaths']).sort_values(by='Avg. Deaths',ascending=False)    
        #vis 1 bar
        fig = plt.figure(figsize=(11,7))
        sns.barplot(y='Risk Factor',x='Avg. Deaths',data=df_left)
        plt.title('Gemiddeld aantal doden per risico factor in ' +options_left)
        plt.xlabel('Gemiddeld aantal doden')
        st.write(fig)
        #vis 2 bar
        max_value = df_left.iat[0, 0]
        fig = plt.figure(figsize=(9,5))
        sns.barplot(x='Year',y=max_value,data=selected_data_left,palette='viridis')
        plt.xticks(rotation=90)
        plt.title("Aantal overleden aan het gevolg van " + max_value + " in " +options_left)
        plt.ylabel('Aantal doden')
        st.write(fig)

        #vis 3 pie
        fig, ax = plt.subplots(figsize=(8,9))
        myexplode = [0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ax.pie(df_left['Avg. Deaths'][:10],labels=df_left['Risk Factor'][:10], autopct='%.1f%%', explode = myexplode, shadow = True)
        ax.set_title('Verdeling % van '+options_left)
        st.pyplot(fig)

        #vis 4 top 3
        lijn1 = df_left.iat[0, 0]
        lijn2 = df_left.iat[1, 0]
        lijn3 = df_left.iat[2, 0]
        fig = plt.figure(figsize=(10,8))
        plt.plot(selected_data_left.Year,selected_data_left[lijn1],label=lijn1)
        plt.plot(selected_data_left.Year,selected_data_left[lijn2],label=lijn2)
        plt.plot(selected_data_left.Year,selected_data_left[lijn3],label=lijn3)
        plt.legend()
        plt.xlabel('Jaar verloop')
        plt.ylabel('Aantal doden')
        plt.title('Aantal doden top 3 in '+options_left)
        st.write(fig) 

    with col2: #right side
        options_right = st.selectbox('Selecteer het tweede land',alles['Country Name'].unique(), index = 33)     
        if options_left == options_right:
            st.error('Selecteer een ander land dat nog niet gekozen is!', icon="🚨")
        else:   
            selected_data_right = alles[alles['Country Name']==options_right]
            risk_factors = [rf for rf in selected_data_right.columns if rf not in ['Country Name','Year', 'latitude', 'longitude','verhouding','Total Deaths', 'Inhabitants', 'Country Code' ]]
            average_deaths = []
            for rf in risk_factors:
                average_deaths.append(selected_data_right[rf].mean())
            df_right = pd.DataFrame(list(zip(risk_factors,average_deaths)),columns=['Risk Factor','Avg. Deaths']).sort_values(by='Avg. Deaths',ascending=False)    
            #vis 1 bar
            fig = plt.figure(figsize=(11,7))
            sns.barplot(y='Risk Factor',x='Avg. Deaths',data=df_right)
            plt.title('Gemiddeld aantal doden per risico factor in ' +options_right)
            plt.xlabel('Gemiddeld aantal doden')
            st.write(fig)
            
            #vis 2
            max_value = df_right.iat[0, 0]
            fig = plt.figure(figsize=(9,5))
            sns.barplot(x='Year',y=max_value,data=selected_data_right,palette='viridis')
            plt.xticks(rotation=90)
            plt.title("Aantal overleden aan het gevolg van " + max_value + " in " +options_right)
            plt.ylabel('Aantal doden')
            st.write(fig)

            #vis 3 pie
            fig, ax = plt.subplots(figsize=(8,9))        
            myexplode = [0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ax.pie(df_right['Avg. Deaths'][:10],labels=df_right['Risk Factor'][:10], autopct='%.1f%%', explode = myexplode, shadow = True)
            ax.set_title('Verdeling % van '+options_right)
            st.pyplot(fig)

            #vis 4 top 3
            lijn1 = df_right.iat[0, 0]
            lijn2 = df_right.iat[1, 0]
            lijn3 = df_right.iat[2, 0]
            fig = plt.figure(figsize=(10,8))
            plt.plot(selected_data_right.Year,selected_data_right[lijn1],label=lijn1)
            plt.plot(selected_data_right.Year,selected_data_right[lijn2],label=lijn2)
            plt.plot(selected_data_right.Year,selected_data_right[lijn3],label=lijn3)
            plt.legend()
            plt.xlabel('Jaar verloop')
            plt.ylabel('Aantal doden')
            plt.title('Aantal doden top 3 in '+options_right)
            st.write(fig)                 




#Page three
if selected == "Kaart":
    col1, col2, col3  = st.columns(3)
    with col1: #left side
        components.html(
        """
            <div style="text-align: left">
            <div name="airvisual_widget" key="63616b2690645e04c0157853"></div>
            <script type="text/javascript" src="https://widget.iqair.com/script/widget_v3.0.js"></script>
            </div>
        """)

    with col2: #middle
        components.html(
        """
            <div style="text-align: center">
            <div name="airvisual_widget" key="63617dba87bcb4e85a7d8656"></div>
            <script type="text/javascript" src="https://widget.iqair.com/script/widget_v3.0.js"></script>
            </div>
        """)
    with col3: #right side
        components.html(
        """
            <div style="text-align: right">
            <div name="airvisual_widget" key="63617e9144e5c873a3f3b473"></div>
            <script type="text/javascript" src="https://widget.iqair.com/script/widget_v3.0.js"></script>
            </div>
        """)

    m = leafmap.Map(tiles="stamentoner", center =(10, -10), zoom = 3 )
    m.add_heatmap(
        alles,
        latitude="latitude",
        longitude="longitude",
        value="Air pollution",
        name="Heat map",
        radius=30,
    )
    m.to_streamlit(height=1000)

    st.title("Heatmap India")
    m = leafmap.Map(tiles="stamentoner", center =(22.930809, 78.313719), zoom = 5 )
    m.add_heatmap(
        india,
        latitude="latitude",
        longitude="longitude",
        value="no2",
        name="Heat map",
        radius=40,
    )
    m.to_streamlit(height=1000)


#Page four
if selected == "Model":
    #Data prep
    IND= alles[alles["Country Name"] == "India"]
    IND['Air_pollution'] = IND['Air pollution'].round()
    IND = IND[IND['Year'] >=2004]
    CH=alles[alles["Country Name"] == "China"]
    CH['Air_pollution'] = CH['Air pollution'].round()
    CH = CH[CH['Year'] >=2004]

    INDCH=pd.concat([IND, CH])
    #vis 1
    country_color_map = {"India": "yellow", "China": "red"}  
    fig = px.scatter(INDCH, x='Year', y='Air_pollution', color='Country Name',  color_discrete_map = country_color_map,  height= 900)
    fig.update_traces(marker={'size': 15})
    fig.update_layout(title='Verloop doden over de jaren heen', yaxis_title='Aantal doden')
    st.plotly_chart(fig, use_container_width=True)

    #vis 2
    fig = go.Figure(data=go.Heatmap(
            z=INDCH.Air_pollution,
            x=INDCH.Year,
            y=INDCH['Country Name'],
            colorscale='Rainbow', colorbar_title = 'Aantal doden'))
    fig.update_layout(title="Aantal doden per jaar door luchtvervuiling in China en India", height = 900)
    st.plotly_chart(fig,use_container_width=True)

    #vis 3
    dood_datum = ols("Air_pollution ~ Year", data=IND).fit()
    explanatory=pd.DataFrame({'Year': np.arange(2003, 2026)})
    prediction=explanatory.assign(Air_pollution=dood_datum.predict(explanatory))
    # Plot 
    fig = px.scatter(IND, x='Year', y='Air_pollution', title= "Voorspelling aantal doden per jaar door air pollution in India", height = 900)
    fig.add_scatter(x=prediction['Year'], y=prediction['Air_pollution'])
    fig.update_traces(marker={'size': 15})
    fig.update_layout(height = 900, yaxis_title='Aantal doden')
    # Show plot 
    st.plotly_chart(fig,use_container_width=True)


