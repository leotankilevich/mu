import strawberry

from app.graphql.query import Query
from app.graphql.mutation import Mutation

from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
