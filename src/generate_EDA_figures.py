# author: Allyson Stoll
# date: 2021-11-25

"""Generate EDA figures for the 522_Ramen project

Usage: generate_EDA_figures.py --path=<path> --out_path=<out_path>

Options:
--path=<path>           The data to process
--out_path=<out_path>   Path (excluding filenames) of where to locally write the file
"""

import os
import pandas as pd
import random

import geopandas as gpd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import altair as alt

from docopt import docopt

opt = docopt(__doc__)

def main(path, out_path):
    df = pd.read_csv(path)

    # Generate CSV of null value
    nulls_df = pd.DataFrame(df.isnull().sum(), columns = ['No. of Nulls'])

    try:
        nulls_df.to_csv(out_path + "/null_counts.csv", index=False)
    except:
        os.makedirs(os.path.dirname(out_path))
        nulls_df.to_csv(out_path + "/null_counts.csv", index=False)

    # Making the ratings histogram
    rating_histo = (
        alt.Chart(df)
        .mark_bar(color="dimgrey")
        .encode(
            alt.X("Stars:Q", bin=alt.Bin(maxbins=20), title="Stars Rating"),
            alt.Y("count()", title="Count"),
        )
        .properties(title="Distribution of Star Ratings")
    )

    try:
        rating_histo.save(out_path + "/stars_histogram.png")
    except:
        os.makedirs(os.path.dirname(out_path))
        rating_histo.save(out_path + "/stars_histogram.png")

    # Making the ramen type histogram
    type_histo = (
        alt.Chart(df)
        .mark_bar(color="dimgrey")
        .encode(
            alt.X("Style:O", sort="-y", title="Ramen Package Style"),
            alt.Y("count()", title="Count"),
        )
        .properties(title="Distribution of Ramen Package Types")
    )

    try:
        type_histo.save(out_path + "/type_histogram.png")
    except:
        os.makedirs(os.path.dirname(out_path))
        type_histo.save(out_path + "/type_histogram.png")

    # Making the ramen variety word cloud
    variety_words = "".join(df["Variety"].tolist())

    def grey_color(word, font_size, position, orientation, random_state=2021, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(0, 50)

    wc_variety = WordCloud(background_color="white", random_state=2021)

    wc_variety.generate(variety_words)

    wc_variety.recolor(color_func=grey_color)

    plt.axis("off")

    try:
        wc_variety.to_file(out_path + "/variety_wordcloud.png")
    except:
        os.makedirs(os.path.dirname(out_path))
        wc_variety.to_file(out_path + "/variety_wordcloud.png")

    # Quick data manipulation for country counts needed for next plot
    ramen_df = pd.DataFrame()
    ramen_df["counts"] = pd.DataFrame(df["code"].value_counts())
    ramen_df.index.name = "code"

    # Creating map of ramen source locations
    # Modeled after blog post on relataly.com on heatmap plotting maps
    # https://www.relataly.com/visualize-covid-19-data-on-a-geographic-heat-maps/291/
    SHAPEFILE = "data/eda/shapefiles_for_eda/ne_110m_admin_0_countries.shp"

    geo_df = gpd.read_file(SHAPEFILE)[["ADMIN", "ADM0_A3", "geometry"]]

    geo_df.columns = ["country", "code", "geometry"]

    geo_df = geo_df.drop(geo_df.loc[geo_df["country"] == "Antarctica"].index)

    geo_df = pd.merge(
        left=geo_df, right=ramen_df, how="left", left_on="code", right_on=ramen_df.index
    )

    # Creating the plot
    title = "Ramen Sources"
    col = "counts"
    vmin = ramen_df[col].min()
    vmax = ramen_df[col].max()
    cmap = "plasma"

    # Create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(20, 8))

    # Remove the axis
    ax.axis("off")
    geo_df.plot(
        column=col,
        ax=ax,
        edgecolor="0.8",
        linewidth=1,
        cmap=cmap,
        missing_kwds=dict(
            color="lightgrey",
        ),
    )

    # Add a title
    ax.set_title(title, fontdict={"fontsize": "25", "fontweight": "3"})

    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)

    # Empty array for the data range
    sm._A = []

    # Add the colorbar to the figure
    cbaxes = fig.add_axes([0.15, 0.25, 0.01, 0.4])
    cbar = fig.colorbar(sm, cax=cbaxes)

    try:
        fig.savefig(out_path + "/ramen_map.png", dpi=300)
    except:
        os.makedirs(os.path.dirname(out_path))
        fig.savefig(out_path + "/ramen_map.png", dpi=300)

if __name__ == "__main__":
    main(opt["--path"], opt["--out_path"])
