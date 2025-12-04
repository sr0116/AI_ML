from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app_graphql.schema import schema
from api.app_dash.dashboard import flask_app

app = FastAPI(
    title="======================== 대시보드 =============================",
    version="1.0.0",
)

#  CORS  개버
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/app_graphql")

app.mount("/dashboard", WSGIMiddleware(flask_app))
