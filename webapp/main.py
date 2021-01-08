
# coding: utf-8

# In[1]:


from bokeh.plotting import figure
from bokeh.io import output_notebook,show
import pandas as pd
from bokeh.models import ColumnDataSource, Div
from bokeh.io import curdoc
import os

output_notebook()


# In[2]:


countries = pd.read_csv(os.path.join(os.getcwd(),
                             '../datasets/countries_of_the_world.csv'),
                        decimal=",")
countries.head()


# In[3]:


countries.describe()


# In[4]:


countries['Country'] = countries['Country'].str.strip()
countries['Region'] = countries['Region'].str.strip()


# In[5]:


regions = list(countries['Region'].unique())
regions.append('ALL')
regions


# In[6]:


source = ColumnDataSource(data=dict(x=[], 
                                    y=[], 
                                    
                                    country=[], 
                                    gdp=[], 
                                    birthrate=[], 
                                    )
                         )


# In[7]:


tooltips = [('Country', '@country'),
            ('GDP per capita', '@gdp'),
            ('Birthrate', '@birthrate')
           ]


# In[8]:


p = figure(plot_height = 300, 
           plot_width = 800, 
           
           x_range = (0, 40000), 
           y_range = (0, 55),
           
           title = 'Birthrate vs GDP per capita', 
           
           toolbar_location = None, 
           
           tooltips = tooltips)


# In[9]:


p.circle(x = 'x', 
         y = 'y', 
         
         source = source, 
         
         size = 7,
         line_color = None, 
         )


# In[10]:


def select_countries():
    
    selected = countries
    region = region_selector.value
    min_gdp = gdp_slider.value
        
    if (region != 'ALL'):
        selected = selected[selected['Region'] == region]
        
    selected = selected[
        (selected['GDP ($ per capita)'] >= min_gdp)]
    
    print('Region = ', region)
    print('Min GDP = ', min_gdp)
    
    return selected


# In[11]:


def update():
    
    df = select_countries()
    print(list(df['Country']))
    
    source.data = dict(
        x=df['GDP ($ per capita)'],
        y=df['Birthrate'],
        country=df["Country"],
        gdp=df['GDP ($ per capita)'],
        birthrate=df['Birthrate']
    )


# In[12]:


from bokeh.models.widgets import Slider, Select


# In[13]:


homepage = Div(text=open(os.path.join(os.getcwd(), 'homepage.html')).read(), width=800)


# In[14]:


region_selector = Select(title = 'Region',
                         options = sorted(regions),
                         value = 'ALL'
               )


# In[15]:


region_selector.on_change('value', lambda attr, old, new: update())


# In[16]:


gdp_slider = Slider(start = 0, 
                    end = 56000, 
                    
                    value = 1, 
                    step = .1,
                    
                    title = 'Minimum GDP per capita')


# In[17]:


gdp_slider.on_change('value', lambda attr, old, new: update())


# In[18]:


from bokeh.layouts import layout, widgetbox


# In[19]:


inputs = widgetbox(region_selector, gdp_slider)


# In[20]:


plot_layout = layout([
    [homepage],
    [inputs],
    [p]
])


# In[21]:


update()


# In[22]:


show(plot_layout)


# In[23]:


curdoc().add_root(plot_layout)
curdoc().title = 'Birthrate vs Per Capita GDP'

