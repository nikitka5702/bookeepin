import graphene

from backend.main.schema import Query

schema = graphene.Schema(query=Query)
