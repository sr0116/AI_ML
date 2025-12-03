import flask
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from plotly.express import treemap

from .graphql_client import fetch_sales_view_all
from .modules.cards import bring_card_data
from .modules.year_bar import year_bar_graph
from .modules.year_month_line import year_month_line_graph

# Flask & Dash
flask_app = flask.Flask(__name__)

dash_app = Dash(
    __name__,
    server=flask_app,
    requests_pathname_prefix="/dashboard/",
    suppress_callback_exceptions=True,
)


# 카드 스타일
def card_style():
    return {
        "flex": "1",
        "margin": "0 10px",
        "padding": "20px",
        "backgroundColor": "#F8F9FA",
        "borderRadius": "10px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
        "textAlign": "center",
    }


# Layout
dash_app.layout = html.Div(
    style={"padding": "20px"},
    children=[

        # 제목
        html.H2("매출 분석 대시보드", style={"textAlign": "center"}),

        # 카드 4개
        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px"},
            children=[
                html.Div(id="card_total_sales", style=card_style(), children=[html.H4("총매출액")]),
                html.Div(id="card_total_profit", style=card_style(), children=[html.H4("전체 순이익")]),
                html.Div(id="card_total_customers", style=card_style(), children=[html.H4("총 고객수")]),
                html.Div(id="card_total_qnty", style=card_style(), children=[html.H4("총 판매수량")]),
            ]
        ),

        # 연도별 매출 + 월별 매출 그래프
        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px"},
            children=[
                html.Div(dcc.Graph(id="chart-year-bar"), style={"flex": "1", "height": "380px"}),
                html.Div(dcc.Graph(id="chart-year-line"), style={"flex": "1", "height": "380px"}),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        # 지역 선택 필터
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px"},
                            children=[
                                dcc.Dropdown(
                                    id="region-filter",
                                    options=[],  # 콜백에서 채워짐
                                    value=None,
                                    placeholder="지역 선택(미선택 시 전체)",
                                    clearable=True,
                                    style={"width": "60%", "fontSize": "12px", "marginLeft": "auto"},
                                )
                            ]
                        ),

                        # 시군구 그래프
                        html.Div(
                            dcc.Graph(id="region-sigungu-chart", style={"width": "100%", "height": "100%"}),
                            style={
                                "display": "flex",
                                "justifyContent": "flex-end",
                                "marginBottom": "6px",
                                "width": "100%",
                            },
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        # 지역 선택 필터
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px"},
                            children=[
                                dcc.Dropdown(
                                    id="category-filter",
                                    options=[
                                        {"label": "제품", "value": "productName"},
                                        {"label": "제품분류", "value": "productCategoryName"},
                                        {"label": "대분류", "value": "categoryName"},
                                    ],  # 콜백에서 채워짐
                                    value=None,
                                    placeholder="지역 선택(미선택 시 전체)",
                                    clearable=True,
                                    style={"width": "60%", "fontSize": "12px", "marginLeft": "auto"},
                                )
                            ]
                        ),

                        # 시군구 그래프
                        html.Div(
                            dcc.Graph(id="category-treemap", style={"width": "100%", "height": "100%"}),
                            style={
                                "display": "flex",
                                "justifyContent": "flex-end",
                                "marginBottom": "6px",
                                "width": "100%",
                            },
                        ),
                    ]
                ),
            ]
        ),

    ]
)


@dash_app.callback(
    [
        Output("card_total_sales", "children"),
        Output("card_total_profit", "children"),
        Output("card_total_customers", "children"),
        Output("card_total_qnty", "children"),
        Output("chart-year-bar", "figure"),
        Output("chart-year-line", "figure"),
        Output("region-filter", "options"),
        Output("region-sigungu-chart", "figure"),
        Output("category-filter", "options"),
        Output("category-treemap", "figure"),
    ],
    [
        Input("region-filter", "value"),
        Input("category-filter", "value"),
    ],
)
def update_dashboard(selected_region, selected_category):
    df = fetch_sales_view_all()

    # 카드 데이터 계산
    cards = bring_card_data(df)

    # 연도별 시각화
    fig_bar = year_bar_graph(df)
    fig_line = year_month_line_graph(df)

    # 지역 옵션
    region_options = [
        {"label": r, "value": r}
        for r in df["region"].drop_duplicates()
    ]

    # 지역 필터 적용
    region_df = df[df["region"] == selected_region] if selected_region else df

    # 시군구 집계
    sigungu_group = (
        region_df.groupby("sigungu", as_index=False)["salesAmount"]
        .sum()
        .sort_values("salesAmount", ascending=False)
    )

    # 시군구 그래프
    fig_region = px.bar(
        sigungu_group,
        x="sigungu",
        y="salesAmount",
        title=f"{selected_region or '전체'} 시군구별 매출"
    )

    # 카테고리 옵션(고정)
    category_options = [
        {"label": "제품", "value": "productName"},
        {"label": "제품분류", "value": "productCategoryName"},
        {"label": "대분류", "value": "categoryName"},
    ]

    # 카테고리 트리맵 (계층형)

    # 선택값에 따라 트리맵 단계 자동 결정
    if selected_category == "categoryName":
        # 1단계 : 대분류만
        treemap_label = "대분류"
        path = ["categoryName"]
        treemap_df = (
            df.groupby(path, as_index=False)["salesAmount"]
            .sum()
            .sort_values("salesAmount", ascending=False)
        )

    elif selected_category == "productCategoryName":
        # 2단계 : 대분류 → 제품분류
        treemap_label = "제품분류"
        path = ["categoryName", "productCategoryName"]
        treemap_df = (
            df.groupby(path, as_index=False)["salesAmount"]
            .sum()
            .sort_values("salesAmount", ascending=False)
        )

    else:
        # 3단계 : 대분류 → 제품분류 → 제품
        treemap_label = "제품"
        path = ["categoryName", "productCategoryName", "productName"]
        treemap_df = (
            df.groupby(path, as_index=False)["salesAmount"]
            .sum()
            .sort_values("salesAmount", ascending=False)
        )

    # 트리맵 색상 (저채도 팔레트 적용)

    custom_colorscale = [
        [0.0, "rgb(230, 242, 255)"],  # 아주 연한 파랑
        [0.3, "rgb(198, 221, 245)"],  # 파스텔톤
        [0.6, "rgb(158, 196, 233)"],  # 중간 블루
        [1.0, "rgb(104, 158, 209)"],  # 진한 블루
    ]

    fig_treemap = px.treemap(
        treemap_df,
        path=path,
        values="salesAmount",
        color="salesAmount",
        title=f"{treemap_label} 기준 매출 트리맵",
        color_continuous_scale=custom_colorscale,
    )
    fig_treemap.update_traces(
        texttemplate="%{label}<br>%{value:,}원",
        hovertemplate="<b>%{label}</b><br>매출: %{value:,}원<extra></extra>"
    )
    fig_treemap.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
        font={"size": 12},
        coloraxis_colorbar=dict(
            title="매출액",
            thickness=10,
            len=0.8
        )
    )

    return (
        [html.H2("총 매출액"), html.H4(f"{cards['total_sales']:,}원")],
        [html.H2("전체 순이익"), html.H4(f"{cards['total_profit']:,}원")],
        [html.H2("총 고객수"), html.H4(f"{cards['total_customers']}명")],
        [html.H2("총 판매수량"), html.H4(f"{cards['total_qnty']}건")],
        fig_bar,
        fig_line,
        region_options,
        fig_region,
        category_options,
        fig_treemap,
    )
