import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]

def draw_line_plot():
    data = df.copy()
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(data.index, data["value"], color="red")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    fig.savefig("line_plot.png")
    return fig

def draw_bar_plot():
    data = df.copy()
    data["year"] = data.index.year
    data["month"] = data.index.month
    data["month_name"] = data.index.strftime("%B")

    df_bar = data.groupby(["year","month","month_name"])["value"].mean().unstack()

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    df_bar = df_bar[months]

    fig = df_bar.plot(kind="bar", figsize=(10,8)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    fig.savefig("bar_plot.png")
    return fig

def draw_box_plot():
    data = df.copy()
    data.reset_index(inplace=True)
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.strftime("%b")
    data["month_num"] = data["date"].dt.month
    data = data.sort_values("month_num")

    fig, axes = plt.subplots(1,2, figsize=(15,5))

    sns.boxplot(x="year", y="value", data=data, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=data, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
