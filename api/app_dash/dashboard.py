import flask
from dash import Dash, html, dcc, Input, Output
from .graphql_client import fetch_sales_view_all

# Dash  라이브러리임
flask_app = flask.Flask(__name__)

dash_app = Dash(
    __name__,
    server=flask_app,
    requests_pathname_prefix='/dashboard/',
    suppress_callback_exceptions=True,
)


def card_style():
    return {
        "flex": "1",
        "margin": "0 10px",
        "padding": "10px",
        "color": "gray",
        "backgroundColor": "white",
        "border": "1px solid gray",
        "textAlign": "center",
        "borderRadius": "8px",
        "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.25)",
        "gap": "12px",
    }


dash_app.layout = html.Div(
    style={'padding': '20px', "backgroundColor": "white"},
    children=[
       html.H2("매출 분석 대시보드", style={'textAlign': 'center', 'color': 'gray'}),
        html.Hr(),
        #   이거 사용해서 하는 방법도 있음
        # dcc.Interval(id="interval_load", interval=1*1000, n_intervals=0),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "30px",

            },
            children=[
                html.Div(id="total_sales", style=card_style(), children=[html.H4('총 매출액'), ]),
                html.Div(id="total_profit", style=card_style(), children=[html.H4('전체 순이익')]),
                html.Div(id="total_customer", style=card_style(), children=[html.H4('총 고객순')]),
                html.Div(id="total_qnty", style=card_style(), children=[html.H4('총 거래건수')]),
            ]
        )
    ]
)


# output: 리턴하는 값, input: 파라미터 받는 값
@dash_app.callback(
    [
        Output("total_sales", "children"),
        Output("total_profit", "children"),
        Output("total_customer", "children"),
        Output("total_qnty", "children"),
    ],
    Input("total_sales", "value"),
)
def update_dashboard(n):
    df = fetch_sales_view_all()
    return (
        [html.H4("총 매출액"), html.H2("1200원")],
        [html.H4("전체 순이익"), html.H2("300원")],
        [html.H4("총 고객수"), html.H2("50명")],
        [html.H4("총 거래건수"), html.H2("80건")],
    )

