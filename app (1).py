# INSTRUCTIONS:
# 1. Open a "Terminal" by: View --> Terminal OR just the "Terminal" through the hamburger menu
# 2. run in terminal with: streamlit run app.py
# 3. click the "Open in Browser" link that pops up OR click on "Ports" and copy the URL
# 4. Open a Simple Browswer with View --> Command Palette --> Simple Browser: Show
# 5. use the URL from prior steps as intput into this simple browser

import streamlit as st

import altair as alt

import plotly.express as px

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

from vega_datasets import data as vega_data


st.title('Tracking the Skyfall: Patterns and Insights from Meteorite Landings')

 

st.text('Group 3: Christian Lee, Sharon Chenli, Celesta Irawan')

st.text('Link to Meteorite Landings Dataset: https://catalog.data.gov/dataset/meteorite-landings')

st. text ('This comprehensive data set from The Meteoritical Society contains information on all of the known meteorite landings.')
 

st.markdown('''The dataset used in this project contains meteorite landing data, which includes detailed

            information about meteorite landings from various parts of the world. By visualizing this data, we

            can understand trends such as when meteorites have fallen, where they have landed, and what characteristics

            they have, such as their mass and classification. One key aspect of this dataset is the temporal dimension,

            showing how meteorite impacts have been recorded over time, as well as the spatial distribution of these

            impacts globally.

            ''')

 

def load_data():

    data = pd.read_csv('Meteorite_Landings.csv')

    data['year'] = pd.to_datetime(data['year'], errors = 'coerce').dt.year

    return data

 

data = load_data()

st.sidebar.header('Filters')

year_filter = st.sidebar.slider('Select Your Range',

                                 int(data['year'].min()),

                                 int(data['year'].max()),

                                 (1900, 2020))

 

mass_filter = st.sidebar.slider('Select Mass Range(grams)',

                                 float(data['mass (g)'].min()),

                                 float(data['mass (g)'].max()),

                                 (0.0, 5000.0))

 

filtered_data = data[(data['year'] >= year_filter[0]) &

                     (data['year'] <= year_filter[1]) &

                     (data['mass (g)'] >= mass_filter[0]) &

                     (data['mass (g)'] <= mass_filter[1])]

 

#interactive visualization #1

st.header('Interactive Visualization: Meteorite Impacts Map')

st.markdown('''

            Explore the spatial distribution of meteorite impacts around the globe.

            Use the filters on the sidebar to refine your exploration by year or mass.

            ''')

 

fig = px.scatter_geo(filtered_data,

                     lat = 'reclat', lon = 'reclong',

                     color = 'fall',

                     size = 'mass (g)',

                     hover_data = ['name', 'year', 'recclass', 'mass (g)'],

                     title = 'Meteorite Impacts Worldwide',

                     projection = 'natural earth')

st.plotly_chart(fig)

 

st.markdown('''

            The first interactive visualization allows users to explore meteorite impacts on a world map. Users

            can adjust the year and mass filters in the siderbar to refind the displayed data, showing meteorite

            landings over specific periods or within specific mass ranges. This visualization not only

            shows the global distribution of meteorite impacts, but also uses color to represent the fall status of each

            meteorite (whether it was observed falling or found after the fall), and the size of each point on the map is

            proportional to the mass of the meteorite. This gives a comprehensive view of meteorite impacts around the world,

            based on the selected filters.

            ''')

 

#interactive visualization #2

st.header('Interactive Visualization: Explore Meteorite Landings Across Time and Class')

st.markdown('''

            Adjust the year range with a slider and choose specific meteorite classifications to filter the data.

            ''')

df = pd.read_csv('Meteorite_Landings.csv')

 

year_range = st.slider('Select Your Range', int(df['year'].min()), int(df['year'].max()), (1800, 2000))

selected_class = st.selectbox('Select Meteorite Class', options = ['All'] + list(df['recclass'].unique()))

 

#filter data

filtered_df = df[

    (df['year'] >= year_range[0]) &

    (df['year'] <= year_range[1]) &

    ((df['recclass'] == selected_class) if selected_class != 'All' else True)

]

 

#create Altair chart

scatter = alt.Chart(filtered_df).mark_circle(size = 60).encode(

    x = alt.X('reclong', title = 'Longtitude'),

    y = alt.Y('reclat', title = 'Latitude'),

    color = alt.Color('recclass', legend = None),

    tooltip = ['name', 'mass (g)', 'year']

).properties(

    title = 'Geographic Distribution of Meteorite Landings',

    width = 800,

    height = 400

).interactive()

 

st.altair_chart(scatter, use_container_width = True)

 

st.markdown('''

            The second interactive visualization provies an overview of meteorite landings across different time periods and

            meteorite classes. Users can adjust the year range and select meteorite classifications from a dropdown

            menu. This enables them to view patterns in meteorite landings over time, as well as understand how

            certain meteorite classes are distributed geographically.

            ''')

 

#interactive visualization #3

st.header('Interactive Visualization: Meteorite Landings by Decade')

st.markdown('''Select a specific decade using the dropdown menu to see the geographic distribution of

            meteorites and explore details like name, mass, year, and location by hovering over the points

            on the map.

            ''')

 

alt.data_transformers.disable_max_rows()

countries = alt.topo_feature(vega_data.world_110m.url, 'countries')

filtered_df['decade'] = (filtered_df['year'] // 10) * 10

 

dropdown = alt.binding_select(options = sorted(filtered_df['decade'].unique(), reverse = True),

                              name = 'Choose Decade:')

select = alt.selection_single(fields = ['decade'], bind = dropdown)

 

background = alt.Chart(countries).mark_geoshape(

    fill = 'white',

    stroke = 'black'

).project(

    type = 'equirectangular'

).properties(

    title = 'Meteorite Landings by Decade',

    width = 900,

    height = 500

)

 

points = alt.Chart(filtered_df).mark_circle(size = 50).encode(

    longitude = 'reclong:Q',

    latitude = 'reclat:Q',

    size = alt.value(50),

    tooltip = ['name', 'id', 'nametype', 'mass (g)', 'fall', 'year', 'GeoLocation'],

    color = alt.value('red')

).add_selection(

    select

).transform_filter(

    select

)

 

chart1 = background + points

st.altair_chart(chart1, use_container_width = True)

 

st.markdown('''

            The third interactive visualization focuses on meteorite landings by decade, using a dropdown menu for users

            to select a specific decade. This visualization is interactive, allowing users to explore how meteorite

            landings have changed over time and in different regions of the world. Each of these visualizations helps

            to build a clearer picture of the global patterns of meteorite impacts.

            ''')

 

#Contextual Visualization 1: Distribution of Meteorite Masses by Decade (Log Scale)

st.header('Contextual Visualization 1: Distribution of Meteorite Masses by Decade (Log Scale)')

st.markdown('''

            The box plot visualizes the distribution of meteorite masses over time, grouped by decade. It

            highlights variations in the size of meteorites recorded in different periods.

            ''')

fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(data=filtered_df, x='decade', y='mass (g)', ax=ax, showfliers=False)

ax.set_yscale('log') 

ax.set_title('Distribution of Meteorite Masses by Century', fontsize=14)

ax.set_xlabel('Decade', fontsize=12)

ax.set_ylabel('Meteorite Mass (g) [Log Scale]', fontsize=12)

 

st.pyplot(fig)

 

st.markdown('''

            The box plot provides a statistical summary of meteorite masses detected in each decade, using a

            logarithmic scale to handle the wide range of mass values. The central box represents the interquartile range

            (IQR), with the median shown as a horizontal line. The whiskers extend to indicate the range of masses

            withint 1.5 times the IQR, while extreme values (outliers) are hidden for clarity. This visualization helps

            identify trends or shifts in meteorite size distributions over time, potentially influenced by changes in detection

            technology or reporting practices.

            ''')

 

#Contextual Visualization 2: Meteorite Classifications Distribution

st.header('Contextual Visualization 2: Meteorite Classifications')

st.markdown('''

            The bar chart displays the distribution of meteorite impacts by their classification.

            It allows users to see which types of meteorites are most common globally.

            ''')

classification_counts = data['recclass'].value_counts().reset_index()

classification_counts.columns = ['recclass', 'count']

fig2 = px.bar(classification_counts.head(10), x = 'recclass', y = 'count',

              title = 'Top 10 Meteorite Classifications',

              labels = {'recclass': 'Classification', 'count': 'Number of Impacts'},

              text = 'count')

fig2.update_traces(texttemplate = '%{text}', textposition = 'outside')

st.plotly_chart(fig2)

 

st.markdown('''

            The second visualization presents a bar chart that shows the distribution of meteorite impacts

            based on their classification. Meteorites are categorized into different classes based on their

            composition, and this chart helps us understand which types of meteorites are most commonly

            found. By displaying the top 10 common metoerite classifications, the chart provides insight into

            the diversity of meteorites that have fallen to Earth. It also helps highlight which types of space

            material that we encounter. Together, these visualizations paint a fuller picture of meteorite

            impacts and their role in our understanding of the universe. 

            

            All of the contextual visualizations were created by our group using our dataset, Meteorite Landings.

            ''')

