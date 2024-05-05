import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
import plotly.express as px
import plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
cf.go_offline()


def get_data() -> pd.DataFrame:
    clean_filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "clean",
        "draft_data_clean.csv",
    )
    df = pd.read_csv(clean_filename)
    return df


def slice_by_pos_and_save(df):
    for pos in df["pos"].unique():
        df_pos = df.loc[df["pos"] == pos]
        pos_filename = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "clean",
            f"{pos}_data.csv",
        )
        df_pos.to_csv(pos_filename, index=False)


def main():
    df = get_data()
    df["total_yrds"] = df["rush_yds"] + df["rec_yds"]
    df["total_td"] = df["rush_td"] + df["rec_td"]

    print(pd.unique(df["pos"]))

    df_wr = df.loc[df["pos"] == "WR"]
    print(df_wr.head())
    df_wr_ag = df_wr[
        [
            "draft_round",
            "rush_att",
            "rush_yds",
            "rush_td",
            "rec_yds",
            "rec_td",
            "total_yrds",
            "total_td",
        ]
    ]
    plot_filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "clean", "wr_plot.png"
    )
    testing_plot = df_wr_ag[["total_yrds", "draft_round"]]

    fig = px.box(
        df_wr_ag,
        x="draft_round",
        y="total_yrds",
        title="Total WR Yards by Draft Round",
        points="all",
    )
    fig.write_image(plot_filename)
    fig.write_html(os.path.splitext(plot_filename)[0] + ".html")

    # scatter_yrds = df_wr_ag.plot.scatter(x="draft_round", y="total_yrds")
    # test_plot = df_wr_ag.plot.box(by="draft_round", column="total_yrds")
    # test_plot.plot.savefig()
    # pl = plt.boxplot(
    #     x=df_wr_ag[["total_yrds", "draft_round"]],
    # )
    # plt.show()

    # # pl.savefig(fname=plot_filename, format="png")
    # # plt.show()

    # testing = df_wr_ag.groupby(["draft_round"])

    # # testing.hist()
    # # plt.show()

    # testing = testing.agg([np.mean, np.std, np.max, np.min])
    # testing.to_csv(
    #     os.path.join(
    #         os.path.dirname(os.path.dirname(__file__)),
    #         "data",
    #         "clean",
    #         "testing_wr.csv",
    #     )
    # )


main()
