
import plotly.express as px



def year_bar_graph(df):
    year_grouph = (df.groupby("year", as_index=False)["salesAmount"]
                   .sum()
                   .sort_values(by="salesAmount")
                   )
    fig_bar = px.bar(
        year_grouph,
        x="year",
        y="salesAmount",

    )

    return fig_bar
