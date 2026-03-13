import altair as alt
import pandas as pd
import panel as pn

# this is necessary to render Altair charts in Panel
pn.extension('vega')

# import data from local CSV file
DATA_URL = 'data/seattle-weather.csv'
df = pd.read_csv(DATA_URL)

# ========= Create Altair Chart =======

def create_scatter(df, yax):
    return alt.Chart(df).mark_circle().encode(
        x='date:T',
        y=yax + ':Q', # use the selected y-axis variable
        color='weather:N',
        tooltip=['date:T', 'weather:N', 'temp_max:Q', 'temp_min:Q', 'precipitation:Q']
    ).properties(
        width=400,
        height=300,
    ).interactive()


chart = create_scatter(df, 'temp_max')

title = pn.pane.Markdown("# Seattle Weather Data", styles={'font-size': '16pt', 'font-weight': 'bold', 'color': '#333'})

layout = pn.Column(title, chart)

# ========= Add Interactivity: Y-Axis Selector =======  

# create a selection widget
yax_select = pn.widgets.Select(name='Y Axis', options=['temp_max','wind','precipitation'])

#bind the selection widget to the chart
bound_plot = pn.bind(create_scatter, df, yax_select)
layout = pn.Column(title, bound_plot, yax_select)

# ========= Add Interactivity: Date Range Slider =======  

# create slider for date range
df['year'] = pd.to_datetime(df['date']).dt.year
years = sorted(df['year'].unique().tolist())
year_min = min(years)
year_max = max(years)

year_range = pn.widgets.RangeSlider(
    start = year_min,
    end = year_max,
    value = (year_min, year_max),
    name = 'Year Range'
)

def create_interactive(df, yax, yr_range):
    df_filtered = df[(df['year'] >= yr_range[0]) & (df['year'] <= yr_range[1])]
    return create_scatter(df_filtered, yax)

bound_plot = pn.bind(create_interactive, df, yax_select, year_range)
layout = pn.Column(title, bound_plot, yax_select, year_range)

# ========= TODO: Add Interactivity: Create a multi-select widget=======  

#Multi-select documentation: https://panel.holoviz.org/reference/widgets/MultiChoice.html

# TODO: create a multi-select widget for weather types
# weather_choice = 

# TODO: bind the multi-select widget to the chart, filtering the data based on the selected weather types
# TODO: first, edit create_interactive above to add filtering based on the selected weather types, and then bind the multi-select widget to the chart:
# bound_plot = 
# layout = 

layout.servable()