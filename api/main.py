from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from app_graphql.schema import schema
from api.app_dash.dashboard import flask_app

app = FastAPI(
    title="======================== 대시보드 =============================",
    version="1.0.0",
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/app_graphql")
# 플라스크랑 fastapi 인공지능에서 알아야 함!
# flask dashboard 연결
app.mount("/dashboard", WSGIMiddleware(flask_app))

@app.get("/")
def read_root():
    return {
        "message": "FastAPI, GraphQL, flask/Dash",
    "graphql" : "/graphql",
    "dashboard" : "/dashboard"
    }
