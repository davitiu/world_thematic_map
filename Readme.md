# World Thematic Map

**World Thematic Map** is a lightweight Python package for creating
interactive choropleth (thematic) world maps from tabular data.

The package is designed to work with **OWID-style CSV datasets** and
their corresponding **JSON metadata files**, enabling fast exploration
and visualization of global indicators such as lead pollution.

---

## Features

- Interactive **choropleth world maps** using Plotly
- Support for multiple CSV datasets with corresponding JSON metadata
- Optional handling of **missing country data**
- Built-in color scales and colorbars
- Built-in histogram plots for data exploration
- Robust error handling for:
  - Missing or non-numeric values
  - Incorrect column names
  - Metadata mismatches

---

## Package Structure
```
world_thematic_map/
├── choromap/
│ ├── init.py
│ └── choromap.py
├── data/
│ ├── *.csv
│ └── *.json
├── demo/
│ └── demo.ipynb
├── README.md
├── requirements.txt
└── LICENSE

```

---

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/davitiu/world_thematic_map.git
cd world_thematic_map
pip install -r requirements.txt
The package can be imported using a local path installation.
```

Usage
Create a choropleth map by initializing the main class with a CSV file
and its corresponding JSON metadata:
To use the choromap package, users can append, modify, or remove OWID-style datasets, as long as the countries.json file remains inside the data directory.


from choromap import ChoroMap

cm = ChoroMap(
    csv_path="data/lead_pollution.csv",
    json_path="data/lead_pollution.json"
)

cm.plot_choropleth()

Missing Data Handling
If show_no_data=True is enabled:

Countries without available data are assigned a placeholder value (-1)

Due to color contrast limitations, data regions may appear
visually similar to low-value regions

Hovering over a country always displays the correct values (-1 for missing data),
ensuring interpretability

Colorscale

Colorscale can be set to built-in colorscale within choromap package or alternatively set to different, plotly's specified colorscale like Magma. When data_based_colorbar is set to True, the color bar within the choropleth maps will display colors based on built-in method, or users can change to alternative colorscales when the keyword colorscale= is set to accordingly.

Demo
A full Jupyter Notebook demonstration is included, showcasing:

Choropleth maps for 8 different datasets

Default vs custom color scales

Missing data handling

Histogram visualizations

Data Sources
The demo datasets are based on publicly available data from
Our World in Data (OWID).

