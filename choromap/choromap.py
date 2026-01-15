import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    
# # JSON file source: https://github.com/mledoze/countries
countries_df = pd.read_json('data/countries.json')


class ChoroMap:
    """
    Class that creates choroplath maps from Our World in data csv
    file datasets and corresponding JSON meta datasets. This package works on multiple files.
    No data handling does not show contrast, but hovering on the areas on the map shows numerical values.
    Contrast is clear without no data.
    """
    global countries_df
    
    def __init__(self, **kwargs):
        # Constructor of datasets, no data, colorscale, colormap tick values, tick text,
        # and upper and lower ranges of colorsacle.
        self.datasets = {}
        self.no_data = {}
        self.colorscale = []
        self.tickvals = []
        self.ticktext = []
        self.zmin = 0
        self.zmax = 0

        # for a single or multiple datasets
        for key, files in kwargs.items():
            try:
                data_file, metadata_file = files
                df = pd.read_csv(data_file)
                mdf = pd.read_json(metadata_file)
                self.datasets[key] = {"data": df, "metadata": mdf}
            except Exception as e:
                print(f"Error Losding dataset {key}: {e}")


    def set_ticks(self, keyword, show_no_data = False):
        """
        This method sets the ticks of the colorbar based on simple statistics of datasets.
        Corresponding median values, upper, middle, and lower bond of tick labels are created based on min,
        median - standard deviation, median, median, median + standard deviation, maximum value of the datasets.
        Corresponding tick values can be shown on a colorscale. In case, show_no_data is set to true, other countries, not included in
        an original datasets will be merged and set to -1 value on a choropleth map.
        """
        mean_tick = float(round(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].mean(), 2))
        median_tick = float(round(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].median(), 2))
        max_tick = float(round(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].max(), 2))
        min_tick = float(round(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].min(), 2))
        std_tick = float(round(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].std(), 2))


        if not show_no_data:
            self.tickvals = [min_tick, round((median_tick - std_tick), 2), median_tick, round((median_tick + std_tick), 2), max_tick]
            self.ticktext = [f"{min_tick}\tminimum", f"{round((median_tick - std_tick), 2)}\tmedian - std", f"{median_tick}\tmedian",
                             f"{round((median_tick + std_tick), 2)}\tmedian + std", f"{max_tick}\tmaximum"]
            self.zmin = min_tick
            self.zmax = max_tick

        else:
            self.tickvals = [-1, round((median_tick - std_tick), 2), median_tick, round((median_tick + std_tick), 2), max_tick]
            self.ticktext = ["No Data", f"{round((median_tick - std_tick), 2)}\tmedian - std", f"{median_tick}\tmedian",
                             f"{round((median_tick + std_tick), 2)}\tmedian + std", f"{max_tick}\tmaximum"]
            self.zmin = -1
            self.zmax = max_tick


    def plot_choropleth(self, keyword, show_no_data=False, data_based_colorbar = False, colorscale="Viridis"):

        """
        Maps global choropleth results based on a numerical CSV datasets, based on OWID CSV file structures. Default colorscale is
        "Viridis" it can be changed and if data_based_colorbar is set to True, the colorbar will be changed to customized colorbar,
        presented in this class.

        """

        self.show_no_data = show_no_data

        if keyword not in self.datasets:
            raise KeyError(f"Dataset {keyword} not found. Check your keywords")

        if (self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].dtype == 'O' or
                self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[1]].dtype == 'float64'):
            raise keyword (f"Dattype {keyword} not found. Check your datatypes")

        if self.show_no_data:
            self.with_no_data(keyword)
            df = self.no_data
        else:
            df = self.datasets

        if data_based_colorbar:
            self.data_col_bar(keyword)
            colorscale = self.colorscale
        else:
            self.colorscale = colorscale

        self.set_ticks(keyword, self.show_no_data)


        data = dict(type = 'choropleth',
                    locations = df[keyword]["data"]['Code'],
                    colorscale= self.colorscale,
                    zmin = self.zmin,
                    zmax = self.zmax,
                    text= df[keyword]["data"]['Entity'], z= df[keyword]["data"].iloc[:,3],
                    colorbar = dict(title= self.datasets[keyword]["metadata"].index[-1], len=2.0, nticks=15, ticks="inside",

                                    tickmode='array', tickvals=self.tickvals,  ticktext=self.ticktext),)
        layout = dict(title = df[keyword]["metadata"].loc["title", "chart"], geo = dict(showframe = True, lakecolor="lightblue",
                                                                                        projection = {'type':'equirectangular'}))
        choromap = go.Figure(data = [data], layout = layout)
        iplot(choromap)


    def data_col_bar(self, keyword):
        """
        Customized colorbar, it scales the dataset with stasistical values and sets the colorscale accordingly.
        """
        # colorscale based on mean, median, standard deviation and max value from the numerical column of the dataframe
        median_color = float(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].median())
        mean_color = float(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].mean())
        max_color = float(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].max())
        std_color = float(self.datasets[keyword]["data"][self.datasets[keyword]["data"].columns[3]].std())
        while median_color > 1:
            median_color /= 10
        while mean_color > 1:
            mean_color /= 10
        while max_color > 1:
            max_color /= 10
        while std_color >1:
            std_color /= 10
        self.colorscale=[
            [0.0, "black"],  # no data color
            [median_color - std_color, "black"],
            [median_color, "black"],  # Midpoint color
            [median_color + std_color, "black"],
            [max_color, "black"],    # Highest value color
        ]

    def with_no_data(self, keyword):

        """
        No data handling method.
        """
        global countries_df
        
        if keyword not in self.datasets:
            raise KeyError(f"Dataset {keyword} not found. Check your keywords")

        # creating a set of the country codes from the countries dataset
        countries_set = set(countries_df[countries_df.columns[4]])
        # the set of the country codes from the column in a CSV file, with numerical values
        lead_countries= set(self.datasets[keyword]["data"].columns[1])
        # finding countries with no data presented
        n_list = countries_set.difference(lead_countries)
        n_list = list(n_list)
        n_list.sort()
        # creating a new dataframe with the countries of no data with name and isoAlpha3 columns
        no_data_countries = countries_df[countries_df[countries_df.columns[4]].isin(n_list)][[countries_df.columns[1], countries_df.columns[4]]]
        # renaming columns to match dataframes
        
        no_data_countries.rename(columns = {countries_df.columns[1]:self.datasets[keyword]["data"].columns[0], countries_df.columns[4]:self.datasets[keyword]["data"].columns[1]}, inplace=True )
        # creating an empty column named "Year"
        no_data_countries["Year"] = np.nan
        # creating a new dataframe with no country data concatinating with lead pollution countries
        no_data_countries[str(self.datasets[keyword]["data"].columns[3])] = -1
        self.no_data[keyword] = {"data":(pd.concat([self.datasets[keyword]["data"],
                                                    no_data_countries, self.datasets[keyword]["data"].iloc[-1:-1]],
                                                   ignore_index=True)),
                                 "metadata":self.datasets[keyword]["metadata"]}


    def plot_bar(self, keyword):

        data = self.datasets[keyword]["data"]
        metadata = self.datasets[keyword]["metadata"]
        entity = data.columns[0]
        lead_values= data.columns[3]

        if data[data.columns[2]].nunique() == 1 and data[lead_values].dtype == 'O':
            data[lead_values].value_counts().plot(kind="bar")
            plt.ylabel("Value counts of all countries in the dataset")
            plt.title(metadata.loc["title"].iloc[0])



        elif data[lead_values].dtype == 'O':
            data.groupby(entity)[lead_values].value_counts(ascending=False).head().plot(kind="bar")
            plt.ylabel("Count")
            plt.title(metadata.loc["title"].iloc[0])



        else:
            sns.barplot(x=lead_values, y=entity, data=data.sort_values(by=lead_values, ascending=False).head(), orient='h')
            plt.title(metadata.loc["title"].iloc[0])





