import flask
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from .graphql_client import fetch_sales_view_all
from .modules.cards import bring_card_data
from .modules.year_bar import year_bar_graph
from .modules.year_month_line import year_month_line_graph

# Flask
flask_app = flask.Flask(__name__)

# Dash
dash_app = Dash(
    __name__,
    server=flask_app,
    requests_pathname_prefix="/dashboard/",
    suppress_callback_exceptions=True,
)

# ===================== 스타일 테마 ======================

COLORS = {
    "bg": "#F5F6FA",
    "card_bg": "#FFFFFF",
    "shadow": "0 4px 12px rgba(0,0,0,0.08)",
    "border": "#E6E6E6",
    "text_dark": "#333333",
    "text_sub": "#777777",
    "primary": "#4A90E2"
}

def page_style():
    return {
        "padding": "25px",
        "backgroundColor": COLORS["bg"],
        "minHeight": "100vh",
        "boxSizing": "border-box"
    }

def card_style():
    return {
        "flex": "1",
        "margin": "0 10px",
        "padding": "22px 18px",
        "backgroundColor": COLORS["card_bg"],
        "borderRadius": "10px",
        "boxShadow": COLORS["shadow"],
        "border": f"1px solid {COLORS['border']}",
        "textAlign": "center",
    }

def graph_container_style():
    return {
        "flex": "1",
        "padding": "15px",
        "backgroundColor": COLORS["card_bg"],
        "borderRadius": "10px",
        "boxShadow": COLORS["shadow"],
        "border": f"1px solid {COLORS['border']}",
        "height": "400px",
    }


# ===================== 레이아웃 ======================

dash_app.layout = html.Div(
    style=page_style(),
    children=[

        html.H2(
            "매출 분석 대시보드",
            style={
                "textAlign": "center",
                "marginBottom": "40px",
                "fontWeight": "700",
                "color": COLORS["text_dark"]
            }
        ),

        # 카드 4개
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "35px",
            },
            children=[
                html.Div(id="card_total_sales", style=card_style()),
                html.Div(id="card_total_profit", style=card_style()),
                html.Div(id="card_total_customers", style=card_style()),
                html.Div(id="card_total_qnty", style=card_style()),
            ]
        ),

        # 연도별/월별 그래프
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "30px",
            },
            children=[
                html.Div(dcc.Graph(id="chart-year-bar"), style=graph_container_style()),
                html.Div(dcc.Graph(id="chart-year-line"), style=graph_container_style()),
            ]
        ),

        # 지역 선택 드롭다운
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "flex-end",
                "marginBottom": "20px",
            },
            children=[
                dcc.Dropdown(
                    id="region-filter",
                    options=[],
                    value=None,
                    placeholder="지역 선택 (미선택 시 전체)",
                    clearable=True,
                    style={
                        "width": '45%',
                        "fontSize": "14px",
                    }
                )
            ]
        ),

        # 지역별 그래프
        html.Div(
            dcc.Graph(id="region-chart"),
            style=graph_container_style(),
        ),
    ]
)

# ===================== 콜백 ======================

@dash_app.callback(
    [
        Output("card_total_sales", "children"),
        Output("card_total_profit", "children"),
        Output("card_total_customers", "children"),
        Output("card_total_qnty", "children"),
        Output("chart-year-bar", "figure"),
        Output("chart-year-line", "figure"),
        Output("region-filter", "options"),
        Output("region-chart", "figure"),
    ],
    Input("region-filter", "value")
)
def update_dashboard(selected_region):

    df = fetch_sales_view_all()
    cardData = bring_card_data(df)

    # 기본 그래프
    fig_bar = year_bar_graph(df)
    fig_line = year_month_line_graph(df)

    # Dropdown 옵션 생성
    regions = df["region"].drop_duplicates().sort_values().tolist()
    region_options = [{"label": r, "value": r} for r in regions]

    # 지역별 그래프
    if selected_region:
        region_df = (
            df[df["region"] == selected_region]
            .groupby("sigungu")["salesAmount"]
            .sum()
            .reset_index()
        )
        region_fig = px.bar(
            region_df,
            x="sigungu",
            y="salesAmount",
            title=f"{selected_region} 시군구별 매출",
        )
    else:
        region_df = (
            df.groupby("region")["salesAmount"]
            .sum()
            .reset_index()
        )
        region_fig = px.bar(
            region_df,
            x="region",
            y="salesAmount",
            title="전체 지역 매출",
        )

    # 카드
    return (
        [html.H4("총매출액", style={"color": COLORS["text_sub"]}),
         html.H2(f"{cardData['total_sales']:,}원", style={"color": COLORS["text_dark"]})],

        [html.H4("전체 순이익", style={"color": COLORS["text_sub"]}),
         html.H2(f"{cardData['total_profit']:,}원", style={"color": COLORS["text_dark"]})],

        [html.H4("총 고객수", style={"color": COLORS["text_sub"]}),
         html.H2(f"{cardData['total_customers']}명", style={"color": COLORS["text_dark"]})],

        [html.H4("총 판매수량", style={"color": COLORS["text_sub"]}),
         html.H2(f"{cardData['total_qnty']}건", style={"color": COLORS["text_dark"]})],

        fig_bar,
        fig_line,
        region_options,
        region_fig,
    )
